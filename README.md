# Network CI/CD

## 概要

ネットワークの設定変更は手作業で行われることが多く、設定ミスによる障害が発生しやすいという課題があります。

それを改善するため、このリポジトリでは以下のコンポーネントを用いてネットワークのCI/CDを実装しました。

- containerlabによる検証環境の自動構築（Arista cEOSを使用）
- Ansibleによる設定の自動投入
- NAPALM + pytestによる状態検証
- Github Actionsによるこれら一連の作業の自動化

## 使用技術

- Python 3.13
- pytest
- NAPALM
- Ansible
- containerlab
- Arista cEOS 4.35.1F
- Github Actions

## 検証用トポロジについて

検証環境は以下のSpine-Leaf構成です。

- Spine 2台
- Leaf 4台
- eBGPアンダーレイ

## 実行フロー

```markdown
GitHubにpush/merge
   ↓
CI Pipeline
   ↓
containerlab (テスト環境)
   ↓
設定適用
   ↓
pytest + NAPALMによる検証
   ↓
手動承認
   ↓
CD Pipeline
   ↓
containerlab (本番環境想定)
   ↓
設定適用
```

## ディレクトリ構造

```markdown
network-cicd/
├── ansible/
├── containerlab/
├── desired_state/
├── network_cicd/
├── tests/
│   ├── unit/
│   └── fabric/
└── .github/workflows/
```

## 期待するネットワーク状態の定義

本プロジェクトでは、ネットワークの理想の状態を定義するファイルとして`desired_state.yml`を用意しています。
pytestはこのファイルとNAPALMで取得したデータを比較し、ネットワークが期待する状態になっていることを確認します。

記述例:

```yaml
devices:
  spine01:
    hostname: spine01
    interfaces:
      Loopback0:
        ip_address: 10.255.0.1/32
    bgp:
      asn: 65000
      neighbors:
        10.0.0.1:
          remote_as: 65100
          description: leaf01
      routes:
        - 10.255.0.2/32
```

このファイルでは、以下の事項について記述しています。

- ホスト名
- インターフェースの説明
- インターフェースのIPアドレス
- BGPのAS番号
- BGPネイバー
- 期待される経路情報

この設計により、テスト内容をテストコードから分離することができ、テスト対象の明確化やCI/CDとの統合を容易化につながります。

## テスト設計

`desired_state.yml`で定義した状態になっていることをpytestで確認しています。

構造化データの取得にはNAPALMを用いていますが、Netmikoなどその他のライブラリへの拡張も想定された作りになっています。

## CI/CD設計

### CIで実施すること

- ユニットテスト
- containerlabにて検証環境のデプロイ
- Ansibleを用いて検証環境に設定を適用
- NAPALM + pytestによるネットワーク状態のテスト

### CDで実施すること

- （CD実行前に）手動での承認
- 本番環境にデプロイ（本リポジトリではcontainerlabで再現）

## ローカル環境での実行方法

### 事前準備

以下がインストールされている必要があります。公式ドキュメントを参考にインストールしてください。

- uv
- containerlab

### 環境のインストール

```shell
git clone https://github.com/kmy4a/network-cicd.git
cd network-cicd
uv sync
```

### 検証環境のデプロイ

```shell
cd containerlab/
containerlab deploy
cd ../ansible/
uv run ansible-playbook playbooks/deploy.yml -i inventory.dev.yml
cd ../
```

### テスト実行

```shell
# ユニットテスト
uv run pytest tests/unit/

# ネットワーク状態のテスト
uv run pytest tests/fabric/
```

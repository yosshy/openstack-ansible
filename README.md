Ansible Playbooks for OpenStack Grizzly
=======================================

吉山 あきら <akirayoshiyama@gmail.com>

本ツールは OSS のオーケストレーションツール「Ansible」
（http://ansible.cc/）を使って OpenStack Grizzly 環境をインストールする
ためのレシピ（Ansible のPlaybook）集です。

本ツールは Darragh O'Reilly の quantum-ansible リポジトリ
（https://github.com/djoreilly/quantum-ansible）をベースとし、主に以下
の変更を加えています。

 * Playbook 群のロール化
 * ネットワーク設定の完全自動化
 * サーバタイプの見直し（frontend, controller, network_gateway,
   compute_backend, volume_backend）
 * オールインワン～５サーバタイプへの柔軟な対応
 * OSアカウント整備、他

環境要件
--------

 * Ansible 1.2 以降
 * メモリ 2GB 以上の x86-64 マシン（１台以上）
 * Ubuntu 12.04.2
 * インターネットに接続可能な環境（HTTP プロキシ使用可能）

ネットワーク環境
----------------

以下の２セグメントが存在するネットワーク環境を想定しています。

 * 外部 LAN (External LAN)  
   エンドユーザが VM や OpenStack Dashboard/API にアクセスする為の LAN
 * 内部 LAN（Internal LAN)  
   OpenStack のコンポーネント群が内部通信に使用する為の LAN

レシピ上、インストール対象の x86-64 マシンに２つのネットワーク・インター
フェース(NIC)があり、それらが以下の通りに接続されている事を想定していま
す。

 * NIC#1 → 内部 LAN
 * NIC#2 → 外部 LAN

インストール手順
----------------

1 は全マシン、2 以降は Ansible 実行マシン上で実施します。

 1. x86-64 マシンに Ubuntu 12.04.2 をインストールします。  外部 LAN ・
    内部 LAN 共に DHCP でも構いませんが、DHCP を使用しない場合はOS イン
    ストール時に各ネットワークのパラメータを設定する必要があります。
 2. Python の開発環境をインストールします。

     ```
     sudo apt-get install -y python-dev
     ```

 3. git で ansible をインストールします。

     ```
     git clone https://github.com/ansible/ansible.git
     cd ansible
     python setup.py build
     sudo -E python setup.py install
     ```

 4. 本ツールを展開します。

     ```
     git clone https://github.com/yosshy/openstack-ansible.git
     cd openstack-ansible
     ```

 5. /etc/hosts に OpenStack インストール先サーバの設定を行います。
 6. hosts_* を参考に ansible_hosts ファイルを作成します。
    hosts_* はそれぞれ以下の構成例です。
    * hosts_allinone : １サーバ構成（オールインワン）
    * hosts_2roles : 制御ノード＋VMホスト構成
    * hosts_3roles : 制御ノード＋VMホスト＋ネットワークゲートウェイ構成
    * hosts_5roles : 制御ノード、VMホスト、ネットワークゲートウェイ、フ
      ロントエンド(API等）、ボリュームホスト構成

    以下は hosts_2roles の例です。
     ```
     [controller]
     ansible2        ←インストール先ホスト名

     [compute_backend]
     ansible3        ←インストール先ホスト名
     ansible4        ←インストール先ホスト名
     ansible5        ←インストール先ホスト名
     ansible6        ←インストール先ホスト名

     [frontend:children]
     controller

     [network_gateway:children]
     controller

     [volume_backend:children]
     controller
     ```
 7. group_vars/all の設定項目を設定します。  
    以下のパラメータは利用環境に合わせて修正して下さい。他のパラメータ
    はデフォルト値で構いません。

     ```
     network_gateway: 192.168.0.254
     network_dns: 192.168.0.254
     http_proxy: http://192.168.12.1:8123/
     ```

 8. Ansible を実行します。  
    SSH パスワードを聞かれるので入力します。
    sudo パスワードも聞かれますが、デフォルト値が SSH パスワードになっ
    ているのでそのまま Enter で構いません。

     ```
     ansible -k -K site.yml
     ```


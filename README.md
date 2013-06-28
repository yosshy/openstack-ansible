Ansible Playbooks for OpenStack Grizzly
=======================================

吉山 あきら <akirayoshiyama@gmail.com>

本ツールは OSS のオーケストレーションツール「Ansible」
（http://ansible.cc/ ）を使って OpenStack Grizzly 環境をインストールする
ためのレシピ（Ansible のPlaybook）集です。

本ツールは Darragh O'Reilly の quantum-ansible リポジトリ
（https://github.com/djoreilly/quantum-ansible ）と
Lorin Hochstein の openstack-ansible-modules
（https://github.com/lorin/openstack-ansible-modules ）をベースに、主に
以下の変更を加えています。

 * Playbook 群のロール的な整理（非ロール）
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

なお、現在のレシピは Ansible 実行マシンとインストール先のマシン群が内部
LAN で接続されている必要があります。外部 LAN で接続されている場合、ネッ
トワークゲートウェイの NIC 設定で通信が切断されてしまい、レシピ実行が失
敗します。

インストール手順
----------------

1 は全マシン、2 以降は Ansible 実行マシン上で実施します。

 1. x86-64 マシンに Ubuntu 12.04.2 をインストールします。  外部 LAN ・
    内部 LAN 共に DHCP でも構いませんが、DHCP を使用しない場合はOS イン
    ストール時に各ネットワークのパラメータを設定する必要があります。

 2. Python の開発環境と pwgen をインストールします。

     ```
     sudo apt-get install -y python-dev pwgen
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

 5. /etc/hosts に OpenStack インストール先サーバの設定を行います。この
    際、各ホストに設定する IP アドレスは内部LAN用である必要があります。

 6. sample_hosts/* を参考に、トップディレクトリに ansible_hosts ファイ
    ルを作成します。* はそれぞれ以下の構成例です。
    * all-in-one : １サーバ構成（オールインワン）
    * 2roles : 制御ノード＋VMホスト構成
    * 3roles : 制御ノード＋VMホスト＋ネットワークゲートウェイ構成
    * 5roles : 制御ノード、VMホスト、ネットワークゲートウェイ、フ
      ロントエンド(API等）、ボリュームホスト構成

    以下は 2roles の例です。
     ```
     [controller]
     ansible2        ←インストール先ホスト名

     [compute_backend]
     ansible3        ←インストール先ホスト名
     ansible4        ←インストール先ホスト名
     ansible5        ←インストール先ホスト名
     ansible6        ←インストール先ホスト名

     [frontend:children]
     controller      ←controller を継承（ansible2）

     [network_gateway:children]
     controller      ←controller を継承（ansible2）

     [volume_backend:children]
     controller      ←controller を継承（ansible2）
     ```

 7. group_vars/all の設定項目を設定します。  以下のパラメータは利用環境
    に合わせて修正して下さい。他のパラメータはデフォルト値で構いません。

     ```
     network_gateway: 192.168.0.254
     network_dns: 192.168.0.254
     http_proxy: http://192.168.12.1:8123/
     ```

     以下の項目が未設定の場合、Playbook 実行中に値を適当に設定しますが、
     更新された all ファイルを途中でリロードする機能が Ansible に無い
     ので、一旦実行が止まります。再実行して下さい。

     ```
     root_db_password
     keystone_db_password
     glance_db_password
     nova_db_password
     quantum_db_password
     cinder_db_password
     nova_identity_password
     ec2_identity_password
     swift_identity_password
     quantum_identity_password
     cinder_identity_password
     admin_token
     admin_password
     primary_controller_host
     primary_frontend_host
     controller_ip
     frontend_int_ip
     frontend_ext_ip
     ```

 8. Ansible を実行します。  

     ```
     ansible-playbook site.yml
     ```

    SSH パスワードを聞かれるので入力します。sudo パスワードも聞かれます
    が、デフォルト値が SSH パスワードになっているのでそのまま Enter で
    構いません。

    SSH パスワード、sudo パスワードが不要な場合、ansible.cfg ファイル中の
    当該パラメータの値を False にして下さい。

謝辞
----

本ツールの作成にあたりお世話になった以下の方々に御礼申し上げます。

 * quantum-ansible リポジトリのメンテナ Darragh O'Reilly。
   Darragh の作品無しでは本ツールは有り得なかったでしょう。
 * openstack-ansible-modules リポジトリのメンテナ Lorin Hochstein。
   Glance/Keystone 用 Ansible モジュールを使わせて頂きました。
 * Ansible 開発元の AnsibleWorks。
   Ansible は使いやすく、希少な OSS オーケストレーションツールです。
 * OpenStack コミュニティ。
   素晴らしい OSS クラウド基盤をありがとう。

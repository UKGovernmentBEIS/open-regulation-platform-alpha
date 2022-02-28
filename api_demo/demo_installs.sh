ADDRESS="127.0.0.1"

show_help() {
    echo "ORP Streamlit App Set-up Script"
    echo "This will install the relevant packages as well as run the Streamlit app"
    echo ""
    echo "USAGE:"
    echo "    ./demo_installs.sh [-a ADDRESS]"
    echo ""
    echo "OPTIONAL ARGUMENTS:"
    echo "    -a ADDRESS"
    echo "        The ip address to be passed through to toc.py (default = 127.0.0.1)"
    exit 1
}

while getopts ":h?:a:" opt; do
    case "$opt" in
    h|\?)
        show_help
        ;;
    a)
        ADDRESS=$OPTARG
        ;;
    esac
done

sudo pip3 install virtualenv
virtualenv orp_env
source orp_env/bin/activate

pip3 install streamlit==1.2.0
pip3 install arrow==1.2.1
pip3 install bs4==0.0.1
pip3 install lxml==4.7.1

sudo apt-get install -y libpq-dev python-dev
pip3 install psycopg2==2.9.2

pip3 install -i https://test.pypi.org/simple/ streamlit-bd-cytoscapejs

docker rm -f --volumes $(docker ps -q --filter ancestor=consumer-api-orp:latest)

./run_demo.sh -a $ADDRESS
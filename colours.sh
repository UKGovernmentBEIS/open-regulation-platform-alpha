
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

function green {
    echo ${green}${1}${reset}
}

function red {
    echo ${red}${1}${reset}
}
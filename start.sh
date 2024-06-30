#!/usr/bin/env bash
#^ Dynamically set the path to the bash interpreter

if [[ ${OS:-} = Windows_NT ]]; then
    echo 'error: Please install bun using Windows Subsystem for Linux'
    exit 1
fi

tildify() {
    if [[ $1 = $HOME/* ]]; then
        local replacement=\~/

        echo "${1/$HOME\//$replacement}"
    else
        echo "$1"
    fi
}

dt_command="dashtrack"

# If the --dev flag is passed, check if $DT_HOME is set, if it is not, set it to the current directory
if [[ "$1" == "--dev" ]]; then
    if [[ ! -d "src" ]]; then
        echo "Please run this script from the root directory of the project."
        exit 1
    fi
    if [[ "$DT_HOME" == "" ]]; then
        export DT_HOME=$(pwd)
        dt_command="./start.sh"
    fi
fi

# Check if the $DT_HOME environment variable is set. Thanks to Bun.sh for this snippet.
if [[ ! "$1" == "--dev" ]] && [[ "$DT_HOME" == "" || ! "$DT_HOME" =~ "libexec" ]]; then
# if [[ "$DT_HOME" == "" ]]; then
    echo "The DT_HOME environment variable is not set or does not contain 'libexec'!"

    install_env=DT_HOME
    quoted_install_dir=$(brew --prefix)/opt/dashtrack/libexec

    echo "The DT_HOME environment variable is not set!"

    case $(basename "$SHELL") in
    fish)
        commands=(
            "set --export $install_env $quoted_install_dir"
        )

        fish_config=$HOME/.config/fish/config.fish
        tilde_fish_config=$(tildify "$fish_config")

        if [[ -w $fish_config ]]; then
            {
                echo -e '\n# DT_HOME Environment Variable'

                for command in "${commands[@]}"; do
                    echo "$command"
                done
            } >>"$fish_config"

            refresh_command="source $tilde_fish_config"
        else
            echo "Manually add the directory to $tilde_fish_config (or similar):"

            for command in "${commands[@]}"; do
                echo "  $command"
            done
        fi
        ;;
    zsh)
        commands=(
            "export $install_env=$quoted_install_dir"
        )

        zsh_config=$HOME/.zshrc
        tilde_zsh_config=$(tildify "$zsh_config")

        if [[ -w $zsh_config ]]; then
            {
                echo -e '\n# DT_HOME Environment Variable'

                for command in "${commands[@]}"; do
                    echo "$command"
                done
            } >>"$zsh_config"

            refresh_command="exec $SHELL"
        else
            echo "Manually add the directory to $tilde_zsh_config (or similar):"

            for command in "${commands[@]}"; do
                echo "  $command"
            done
        fi
        ;;
    bash)
        commands=(
            "export $install_env=$quoted_install_dir"
        )

        bash_configs=(
            "$HOME/.bashrc"
            "$HOME/.bash_profile"
        )

        if [[ ${XDG_CONFIG_HOME:-} ]]; then
            bash_configs+=(
                "$XDG_CONFIG_HOME/.bash_profile"
                "$XDG_CONFIG_HOME/.bashrc"
                "$XDG_CONFIG_HOME/bash_profile"
                "$XDG_CONFIG_HOME/bashrc"
            )
        fi

        set_manually=true
        for bash_config in "${bash_configs[@]}"; do
            tilde_bash_config=$(tildify "$bash_config")

            if [[ -w $bash_config ]]; then
                {
                    echo -e '\n# DT_HOME Environment Variable'

                    for command in "${commands[@]}"; do
                        echo "$command"
                    done
                } >>"$bash_config"

                refresh_command="source $bash_config"
                set_manually=false
                break
            fi
        done

        if [[ $set_manually = true ]]; then
            echo "Manually add the directory to $tilde_bash_config (or similar):"

            for command in "${commands[@]}"; do
                echo "  $command"
            done
        fi
        ;;
    *)
        echo 'Manually add the directory to ~/.bashrc (or similar):'
        echo "  export $install_env=$quoted_install_dir"
        ;;
    esac
    echo "To finish installation, run: $refresh_command"
    exit 0
fi

# Check if $1 == "--dev", if it is, clear $1
if [[ "$1" == "--dev" ]]; then
    shift
fi

export CECHO=$(realpath $DT_HOME/src/utils/shell/echo.sh)
export ARTIFACT_HOME_DIR=$DT_HOME/infra/artifacts

cecho() {
    ${CECHO} "$@"
}

# Set architecture
arch=$(uname -s)

help() {
    cat <<EOF

DashTrack 0.0.0
Track your DoorDash trends!

Usage: $dt_command [OPTIONS]

OPTIONS:
    -c, --clean
        Clean up cache and daemon files

    -f, --fix <service>
        Fix any broken trapp service. Currently supported services:
            colima
            redis

    --build-dependencies
        Build pip3 dependencies for trapp on the current system

    -h, --help
        Print help and exit

    -v, --version
        Print version, help and exit

EOF
}

quit() {
    error=$@
    # Unset all variables
    unset arch
    unset ARGFLAG
    unset ARTIFACT_HOME_DIR
    unset DT_PYTHON
    unset DT_PIP
    # deactivate
    if [[ "$error" != "" ]]; then
        cecho -c red -t "Program exited with error."
        cecho -c red -t "Error: $error"
        help
        exit 1
    else
        # Exit program
        cecho -c green -t "Program exited."
    fi
    exit 0
}

have_requirments_changed() {
    if [ ! -f "$DT_HOME/requirements.txt" ]; then
        quit "requirements.txt not found!"
    fi

    # If the requirements_hash file does not exist, return 1
    if [ ! -f "$DT_HOME/infra/artifacts/requirements_hash" ]; then
        return 1
    fi

    current_hash=$(sha256sum $DT_HOME/requirements.txt | awk '{print $1}')
    previous_hash=$(cat $DT_HOME/infra/artifacts/requirements_hash)

    if [[ "$current_hash" == "$previous_hash" ]]; then
        return 1
    else
        return 0
    fi
}

clean() {
    echo "Cleaning up..."
    cecho -c green -t "Removing preview files..."
    # Check if there are any preview files
    preview_files=$(find $DT_HOME -type f -name "*.preview" -print)
    if [[ "$preview_files" == "" ]]; then
        echo "No preview files found!"
    else
        echo "The following files will be deleted:"
        echo "$preview_files"
        read -p "Are you sure you want to delete these files? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            find $DT_HOME -type f -name "*.preview" -delete
            echo "Deleted preview files!"
        else
            echo "Preview files not deleted!"
        fi
    fi
    cecho -c green -t "Removing dependencies..."
    dependencies=($DT_HOME/env $DT_HOME/bin $DT_HOME/logs $DT_HOME/__pycache__ $DT_HOME/.cache $DT_HOME/infra/build/formula/out)
    # Check if requirements have changed
    have_requirments_changed
    if [ $? -eq 0 ]; then
        echo "Requirements have changed. Removing cached dependencies..."
        dependencies+=($DT_HOME/infra/artifacts)
    fi
    for dependency in "${dependencies[@]}"; do
        if test -d "$dependency"; then
            echo "Removing $dependency"
            rip $dependency
        fi
    done
    cecho -c green -t "Done!"
    echo
}

# Check if --help or -h is passed as an argument
if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]] || [[ "$1" == "-v" ]] || [[ "$1" == "--version" ]]; then
    help
    quit
fi

# Check if --clean or -c is passed as an argument
if [[ "$1" == "-c" ]] || [[ "$1" == "--clean" ]]; then
    clean
    quit
fi

# Create logs, .cache, bkp, and bin directories in one go if none exist
if ! test -d "$DT_HOME/logs" || ! test -d "$DT_HOME/.cache" || ! test -d "$DT_HOME/bin"; then
    cecho -c yellow -t "Creating directories..."
    mkdir -p $DT_HOME/logs $DT_HOME/.cache $DT_HOME/bin
fi

# Check if we are in a virtual environment
# Check if python3 in virtual environment exists
if ! command -v $DT_HOME/env/bin/python3 &>/dev/null; then
    cecho -c yellow -t "Virtual environment not found. Creating a new environment..."
    python3 -m venv $DT_HOME/env
    cecho -c green -t "New virtual environment created!"
else
    cecho -c green -t "Virtual environment found!"
fi

export DT_PYTHON=$DT_HOME/env/bin/python3 # Set python3 in virtual environment
export DT_PIP=$DT_HOME/env/bin/pip3 # Set pip3 in virtual environment

# Check if --build-dependencies is passed as an argument
if [[ "$1" == "--build-dependencies" ]]; then
    $DT_HOME/src/utils/shell/build_dependencies.sh
    quit
fi

# Check if requirements are satisfied in virtual environment
output=$($DT_HOME/env/bin/python3 $DT_HOME/tests/test_requirements.py)
if [ $? -ne 0 ]; then
    cecho -c yellow -t "Error: python3 ./tests/test_requirements.py failed with output^"
    echo "Dependency requirements not satisfied. Installing dependencies..."
    $DT_HOME/src/utils/shell/load_dependencies.sh
else
    cecho -c green -t "All dependencies are present!"
fi

if [[ "$(docker ps 2>&1)" =~ "Cannot connect to the Docker daemon" ]]; then
    if [[ $arch == "Darwin" ]]; then
        # Ask user to install Docker Desktop
        cecho -c yellow -t "Docker runtime not detected. Please start or install Docker Desktop to use DashTrack."
    elif [[ $arch == "Linux" ]]; then
        cecho -c yellow -t "Docker runtime not detected. Starting runtime (docker engine)..."
        sudo service docker start
    else
        quit "Invalid architecture: $arch. trapp is only supported on x86_64 and arm64 versions of Darwin and Linux."
    fi
else
    cecho -c green -t "Docker runtime found!"
fi

# Check if Google Chrome is installed on system (only required for autofill)
if [[ "$arch" == "Linux" ]]; then
    chrome_ver=$(google-chrome --version)
    if [[ "$chrome_ver" == "" ]]; then
        # Ask user to install Google Chrome
        cecho -c yellow -t "Google Chrome was not found, do you want to install it? Google Chrome is also required for Ubuntu Server users."
        install_chrome_choice=$(./bin/gum choose "YES" "NO")
        if [[ "$install_chrome_choice" == "YES" ]]; then
            cecho -c yellow -t "Google Chrome was not found. Installing..."
            wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
            sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
            sudo apt update
            sudo apt -y install google-chrome-stable
            chrome_ver=$(google-chrome --version)
        else
            quit "Google Chrome was not installed. Please install Google Chrome manually."
        fi
    else
        export DT_CHROME_VER=$chrome_ver
        cecho -c green -t "Google Chrome found!"
    fi
elif [[ "$arch" == "Darwin" ]]; then
    chrome_ver=$(/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version)
    if [[ "$chrome_ver" == "" ]]; then
        # Ask user to install Google Chrome
        cecho -c yellow -t "Google Chrome was not found, do you want to install it using Homebrew?"
        install_chrome_choice=$(gum choose "YES" "NO")
        if [[ "$install_chrome_choice" == "YES" ]]; then
            cecho -c yellow -t "Installing Google Chrome..."
            brew install --cask google-chrome
            chrome_ver=$(/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version)
        else
            cecho -c yellow -t "Google Chrome was not installed. Please install Google Chrome manually."
        fi
    else
        export DT_CHROME_VER=$chrome_ver
        cecho -c green -t "Google Chrome found!"
    fi
else
    quit "Invalid architecture: $arch. DashTrack is only supported on x86_64 and arm64 versions of Darwin and Linux."
fi

# Check post-install
if [[ "$chrome_ver" == "" ]]; then
    # Ask user to install Google Chrome
    cecho -c yellow -t "Google Chrome was not installed. Please install Google Chrome manually."
else
    export DT_CHROME_VER=$chrome_ver
fi

# Check if chrome-driver is installed in bin/chrome-driver
if [ -d "$DT_HOME/bin/chrome-driver" ]; then
    cecho -c green -t "Chrome driver found!"
else
    cecho -c yellow -t "Chrome driver not found. Installing..."
    mkdir $DT_HOME/bin/chrome-driver
    $DT_HOME/env/bin/python3 $DT_HOME/src/utils/install_chrome_driver.py
    # Check if the script ran successfully
    if [ $? -ne 0 ]; then
        # rm -rf bin/chrome-driver
        quit "scripts/utils/install_chrome_driver.py failed. Please check the logs for more information."
    fi
fi

echo
ARGFLAG=0

while [[ $# -gt 0 ]]; do
    case $1 in
    -f | --fix)
        shift # Remove the --fix argument
        service=$1
        if [[ "$service" == "" ]]; then
            quit "No service specified!"
        fi
        cecho -c yellow -t "Fixing $service..."
        if [[ "$service" == "colima" ]]; then
            status=$(limactl list | grep colima | awk -F' ' '{print $2}')
            cecho -c yellow -t "Colima cotainer status: $status"
            if [[ "$status" == "Broken" ]]; then
                limactl factory-reset colima
                status=$(limactl list | grep colima | awk -F' ' '{print $2}')
                if [[ "$status" == "Broken" ]]; then
                    quit "Failed to fix colima!"
                else
                    cecho -c green -t "Colima fixed!"
                fi
            else
                cecho -c green -t "Colima is not broken!"
                quit
            fi
        elif [[ "$service" == "redis" ]]; then
            docker_redis_metadata=$($DT_PYTHON -c "import sys; sys.path.append('$DT_HOME'); from constants import REDIS_CONTAINER_NAME, REDIS_DATA_DIR; print(REDIS_CONTAINER_NAME, REDIS_DATA_DIR)")
            container_name=$(echo $docker_redis_metadata | awk -F' ' '{print $1}')
            data_volume_name=$(echo $docker_redis_metadata | awk -F' ' '{print $2}')
            status=$(docker inspect -f '{{.State.Status}}' "$container_name" 2>&1)
            cecho -c yellow -t "Redis container status: $status"
            if [[ "$status" =~ "No such object" ]]; then
                quit "No redis service found to fix!"
            else
                # Stop and remove redis container
                docker rm -f $container_name 2>&1
                docker volume rm $data_volume_name 2>&1
                cecho -c green -t "Redis container removed!"
                cecho -c green -t "To restart redis, run trapp again."
            fi
            quit
        else
            quit "Invalid service: $service"
        fi
        ;;
    *)
        quit "Invalid option: $arg"
        ;;
    esac
    shift
done
if [ $ARGFLAG -eq 0 ]; then
    $DT_PYTHON $DT_HOME/src/main.py
fi
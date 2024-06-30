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

# If the --dev flag is passed, check if $DT_HOME is set, if it is not, set it to the current directory
if [[ "$1" == "--dev" ]]; then
    if [[ ! -d "src" ]]; then
        echo "Please run this script from the root directory of the project."
        exit 1
    fi
    if [[ "$DT_HOME" == "" ]]; then
        export DT_HOME=$(pwd)
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

cecho_path=$(realpath $DT_HOME/src/utils/shell/echo.sh)
chmod +x $cecho_path
cecho() {
    ${cecho_path} "$@"
}

# Set architecture
arch=$(uname -s)

help() {
    cat <<EOF

DashTrack 0.0.0
Track your DoorDash trends!

Usage: ./start.sh [OPTIONS]

OPTIONS:  
    -h, --help
        Print help and exit

EOF
}

clean() {
    echo "Cleaning up..."
    echo -e "Removing .cache\nRemoving logs\nRemoving temp infra files"
    rip $DT_HOME/.cache $DT_HOME/bkp/logs $DT_HOME/infra/artifacts $DT_HOME/infra/build/formula/out 2>/dev/null
    echo "Removing preview files..."
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
    echo "Removing dependencies..."
    dependencies=($DT_HOME/env $DT_HOME/bin $DT_HOME/logs $DT_HOME/__pycache__)
    for dependency in "${dependencies[@]}"; do
        if test -d "$dependency"; then
            echo "Removing $dependency"
            rip $dependency
        fi
    done
    echo
}

quit() {
    error=$@
    # Unset all variables
    unset arch
    unset ARGFLAG
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

# Check if --help or -h is passed as an argument
if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    help
    exit 0
fi

# Check if --clean or -c is passed as an argument
if [[ "$1" == "-c" ]] || [[ "$1" == "--clean" ]]; then
    clean
    exit 0
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

# Check if --build-dependencies is passed as an argument
if [[ "$1" == "--build-dependencies" ]]; then
    $DT_HOME/src/utils/shell/build_dependencies.sh
    exit 0
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
    *)
        quit "Invalid option: $arg"
        ;;
    esac
    shift
done
if [ $ARGFLAG -eq 0 ]; then
    $DT_HOME/env/bin/python3 $DT_HOME/main.py
fi
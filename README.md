# DashTrack

**Note**: As of this writing, DashTrack is only supported on Unix systems (MacOS & Linux primarily). We intend to introduce support for Windows in the future.

## &#x26a0;&#xfe0f; Installation (WIP)

In its current iteration, this method will not work. We are still in the process of setting up a reliable distribution target.

```
brew tap KartavyaSharma/DashTrack-Homebrew
brew install dashtrack
```

## Installation (for developers)

Run the following commands to install the nessasary brew packages.

```
brew install bash coreutils gum docker gawk unzip gnu-tar bat wget rm-improved colima openssl@1.1 python-setuptools
```

```
git clone https://github.com/KartavyaSharma/DashTrack.git
cd DashTrack
```

To start DashTrack, run the following dev command:
```
./start.sh --dev
```
**Note**: The `dashtrack` command will not reflect any changes you make to the cloned repository. You will need to use the dev command to test your changes.
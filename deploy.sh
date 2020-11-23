# This script will automatically deploy a website to setup its environment,
# databases, etc. to efficiently make the website runnable on the host.

# This only works if it is called from within its own directory,
# because it is impossible to reliably determine paths relative to a script.
source "./deploy/setup.sh"

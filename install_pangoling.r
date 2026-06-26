# Install pangoling and python environment
install.packages("pangoling", repos = "https://cloud.r-project.org")

pangoling::install_py_pangoling(
    method = "conda",
    # envname = "r_semantic",
    version = "3.11.0"
)

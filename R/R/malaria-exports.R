# Export the "IntrahostComponent" C++ class by explicitly requesting IntrahostComponent be
# exported via roxygen2's export tag.
#' @export IntrahostComponent

# Load the Rcpp module exposed with RCPP_MODULE( ... ) macro.
loadModule(module = "MalariaIntrahostEx", TRUE)

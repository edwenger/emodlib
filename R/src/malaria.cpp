/**
 * @file
 * @brief emodlib malaria Rcpp bindings.
*/

#include <Rcpp.h>

#include "emodlib/malaria/IntrahostComponent.h"

using namespace emodlib::malaria;

RCPP_MODULE(MalariaIntrahostEx){
    Rcpp::class_<IntrahostComponent>("IntrahostComponent")
    //.constructor<>()  // exportable if constructor is made public
    .method("update", &IntrahostComponent::Update)
    .method("challenge", &IntrahostComponent::Challenge)
    .method("treat", &IntrahostComponent::Treat)
    .property("parasite_density", &IntrahostComponent::GetParasiteDensity)
    .property("gametocyte_density", &IntrahostComponent::GetGametocyteDensity)
    .property("fever_temperature", &IntrahostComponent::GetFeverTemperature);
}

// Rcpp doesn't support static methods -- Create() + Configure()
// Expose as module-level functions as below:

// [[Rcpp::export]]
IntrahostComponent* create_intrahost_component() {
    return IntrahostComponent::Create();
}

// [[Rcpp::export]]
void configure_intrahost_component() {
    return IntrahostComponent::params::Configure();
}

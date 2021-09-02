/**
 * @file IntrahostComponent.cpp
 *
 * @brief Malaria intrahost component implementation
 */

#include "IntrahostComponent.h"


namespace emodlib
{

    namespace malaria
    {

        int IntrahostComponent::params::randomSeed = 0;
    
        int IntrahostComponent::params::falciparumMSPVars = DEFAULT_MSP_VARIANTS;
        int IntrahostComponent::params::falciparumNonSpecTypes = DEFAULT_NONSPECIFIC_TYPES;
        int IntrahostComponent::params::falciparumPfEMP1Vars = DEFAULT_PFEMP1_VARIANTS;
    
    
        std::shared_ptr<RANDOMBASE> IntrahostComponent::p_rng = nullptr;

    
        void IntrahostComponent::params::Configure(const ParamSet& pset)
        {
            // TODO: configure top-level params
            
            IntrahostComponent::p_rng = std::shared_ptr<RANDOMBASE>(new PSEUDO_DES(randomSeed, 256));
            
            Infection::params::Configure(pset["infection_params"]);
            Susceptibility::params::Configure(pset["susceptibility_params"]);
        }
    
    
        IntrahostComponent::IntrahostComponent()
            : susceptibility(nullptr)
            , infections()
        {

        }

        IntrahostComponent* IntrahostComponent::Create()
        {
            IntrahostComponent* ic = new IntrahostComponent();
            ic->susceptibility = Susceptibility::Create();
            return ic;
        }

        void IntrahostComponent::Update()
        {
            susceptibility->Update();

            for (auto* inf : infections) {
                inf->Update();
            }
        }

        void IntrahostComponent::Challenge()
        {
            Infection* inf = Infection::Create(susceptibility);
            infections.push_back(inf);
        }

        void IntrahostComponent::Treat()
        {
            infections.clear();
        }

        float IntrahostComponent::GetParasiteDensity() const
        {
            float total = 0.0f;
            for (auto* inf: infections) {
                total += inf->GetParasiteDensity();
            }
            return total;
        }

        float IntrahostComponent::GetGametocyteDensity() const
        {
            float total = 0.0f;
            for (auto* inf: infections) {
                total += inf->GetGametocyteDensity();
            }
            return total;
        }

        float IntrahostComponent::GetFeverTemperature() const
        {
            return susceptibility->GetFeverTemperature();
        }

    }

}

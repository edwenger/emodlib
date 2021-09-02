// suids provides services for creating and manipulating a set of lightweight IDs
// unique to a simulation (Simulation Unique ID ~ suid) in a system distributed on multiple processes

#pragma once

#include "stdint.h"

namespace emodlib
{

    namespace suids
    {
        /*
        Note for users:
        The child object id system can choose a storage size appropriate to the size of the problem.
        To keep lightweight objects lightweight, we allow of the possibility of relatively short (eg 32bit) identities.
        This may have significant performance advantages in cases where objects may need to track, record, and reports
        on the ids of multiple other objects.
        32bits is the default which will be fine for most systems that have << (2 billion)/numtasks of any
        entity type over their lifetime.
        The suid class was originally designed after the boost::uuid interface.
        */

        typedef uint32_t suid_data_t;

        // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        // !!! The 'final' tag is intended to stop developers from adding virtual methods to
        // !!! this class and then extending it.  suid is used everywhere and adding virtual methods
        // !!! adds a vtable pointer (8-bytes) to every instance.  This is really impactful when talking
        // !!! about 100's of millions of mosquitos.
        // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        class suid final
        {
        public:

            // for consistency with boost::uuid, define a special NULL suid.
            // NB: non-nil generating generators must never return an suid with data==0!
            bool is_nil() const { return data == 0; }

            suid_data_t data;

        };

        // standard operators
        inline bool operator==(suid const& lhs, suid const& rhs) { return lhs.data == rhs.data; }
        inline bool operator!=(suid const& lhs, suid const& rhs) { return lhs.data != rhs.data; }
        inline bool operator<(suid const& lhs, suid const& rhs)  { return lhs.data <  rhs.data; }
        inline bool operator>(suid const& lhs, suid const& rhs)  { return lhs.data >  rhs.data; }
        inline bool operator<=(suid const& lhs, suid const& rhs) { return lhs.data <= rhs.data; }
        inline bool operator>=(suid const& lhs, suid const& rhs) { return lhs.data >= rhs.data; }

        // generators - patterned after boost uuid generators

        struct nil_generator
        {
            typedef suid result_type;

            suid operator()() const { suid nil; nil.data =0; return nil; }
        };
        inline suid nil_suid() { nil_generator ng; return ng(); }

        // for lightweight id objects we want to track by category and maintain some process-specific history
        class distributed_generator
        {
        public:
            typedef suid result_type;

            distributed_generator(int _rank, int _numtasks);

            suid operator()();

        private:
            suid next_suid;
            int rank;
            int numtasks;
        };
    
    } // namespace emodlib::suids

} // namespace emodlib

"""Script to be invoked by GDB for testing optimizer pretty printers.
"""

import gdb
import traceback
try:
    from buildscripts.gdb.optimizer_printers import ABTPrinter
except Exception as err:
    gdb.write('TEST FAILED -- {!s}\n'.format(traceback.format_exc()))
    gdb.execute('quit 1', to_string=True)

def verify_type_lookup(type_name):
    try:
        gdb_type = lookup_type(type_name)
        assert gdb_type is not None, 'Failed to lookup type: ' + type_name
        gdb.write('TEST PASSED (lookup type ' + type_name + ')\n')
    except Exception:
        gdb.write('TEST FAILED (type: ' + type_name + ') -- {!s}\n'.format(traceback.format_exc()))
        gdb.execute('quit 1', to_string=True)

gdb.execute('break main')
gdb.execute('run')

# These types are pretty printed entirely in python, so just verify that we're able to lookup the type.
verify_type_lookup(ABTPrinter.build_abt_type())
verify_type_lookup("mongo::optimizer::ABT")
verify_type_lookup("mongo::optimizer::ResidualRequirement")
verify_type_lookup(
    ("mongo::optimizer::algebra::PolyValue<" +
        "mongo::optimizer::BoolExpr<mongo::optimizer::ResidualRequirement>::Atom, " +
        "mongo::optimizer::BoolExpr<mongo::optimizer::ResidualRequirement>::Conjunction, " +
        "mongo::optimizer::BoolExpr<mongo::optimizer::ResidualRequirement>::Disjunction>"),
)
verify_type_lookup("mongo::optimizer::StrongStringAlias<mongo::optimizer::FieldNameAliasTag>")
verify_type_lookup("mongo::optimizer::FieldProjectionMap")

# The following types rely on a C++ function in the mongod binary to pretty print, however certain
# build configurations may optimize out these functions. For now, just assert on whether the type
# exists.
verify_type_lookup("mongo::optimizer::IntervalRequirement")
verify_type_lookup("mongo::optimizer::CompoundIntervalRequirement")
verify_type_lookup(
    ("mongo::optimizer::algebra::PolyValue<" +
        "mongo::optimizer::BoolExpr<mongo::optimizer::IntervalRequirement>::Atom, " +
        "mongo::optimizer::BoolExpr<mongo::optimizer::IntervalRequirement>::Conjunction, " +
        "mongo::optimizer::BoolExpr<mongo::optimizer::IntervalRequirement>::Disjunction>"),
)
verify_type_lookup("mongo::optimizer::cascades::Memo")
verify_type_lookup("mongo::optimizer::PartialSchemaRequirements")
verify_type_lookup("mongo::optimizer::CandidateIndexEntry")

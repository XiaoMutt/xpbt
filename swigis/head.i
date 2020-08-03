%module xpbt
%include "std_string.i"
%include "std_vector.i"
%include "stdint.i"
%include "exception.i"

namespace std{
        %template(IntVector) vector<int>;
}

/* Exception wrappers must be defined before the class::function */
%exception{
try {
    $action
    } catch(ValueError &e) {
    SWIG_exception(SWIG_ValueError, e.what());
    } catch(std::runtime_error &e) {
    SWIG_exception(SWIG_RuntimeError, e.what());
    } catch(...){
    SWIG_exception(SWIG_UnknownError, "Unknown Error");
    }
};
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <cpuid.h>


static PyObject* cpuid(PyObject* self, PyObject* args)
{
    unsigned int level;
    unsigned int eax, ebx, ecx, edx;

    if (!PyArg_ParseTuple(args, "I:cpuid", &level)) {
        return NULL;
    }

    int result = __get_cpuid(level, &eax, &ebx, &ecx, &edx);
    if (result == 0) {
        PyErr_Format(PyExc_ValueError, "Unsupported MSR: 0x%08x", level);
        return NULL;
    }

    return Py_BuildValue("IIII", eax, ebx, ecx, edx);
}


static PyMethodDef CpuidMethods[] = {
    {"cpuid",  cpuid, METH_VARARGS, "Call cpuid. Returns the result as a tuple of (eax, ebx, ecx, edx)."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef cpuid_bindings_module = {
    PyModuleDef_HEAD_INIT,
    "cpuid.bindings",   /* name of module */
    "Use the cpuid instruction from Python", /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    CpuidMethods
};

PyMODINIT_FUNC
PyInit_bindings(void)
{
    return PyModule_Create(&cpuid_bindings_module);
}

import os


router = {
    "global_pep": {
        "host": os.environ.get("GLOBAL_PEP_HOST", 'localhost'),
        "port": int(os.environ.get("GLOBAL_PEP_PORT", 5001)),
    },
    "logger": {
        "host": os.environ.get("GLOBAL_PEP_HOST", 'localhost'),
        "port": int(os.environ.get("GLOBAL_PEP_PORT", 5002)),
    },
    "tenants": {
        "a": {
            "pep": {
                "host": os.environ.get("TENANT_A_PEP_HOST", 'localhost'),
                "port": int(os.environ.get("TENANT_A_PEP_PORT", 5010)),
            },
            "hosts": {
                "host1": {
                    "host": os.environ.get("TENANT_A_HOST1_HOST", 'localhost'),
                    "port": int(os.environ.get("TENANT_A_HOST1_PORT", 5011)),
                },
                "host2": {
                    "host": os.environ.get("TENANT_A_HOST2_HOST", 'localhost'),
                    "port": int(os.environ.get("TENANT_A_HOST2_PORT", 5012)),
                },
                "host3": {
                    "host": os.environ.get("TENANT_A_HOST3_HOST", 'localhost'),
                    "port": int(os.environ.get("TENANT_A_HOST3_PORT", 5013)),
                }
            },
            "nfv": {
                "host": os.environ.get("TENANT_A_NFV_HOST", 'localhost'),
                "port": int(os.environ.get("TENANT_A_NFV_PORT", 5019)),
            }
        },
        "b": {
            "pep": {
                "host": os.environ.get("TENANT_B_PEP_HOST", 'localhost'),
                "port": int(os.environ.get("TENANT_B_PEP_PORT", 5020)),
            },
            "hosts": {
                "host1": {
                    "host": os.environ.get("TENANT_B_HOST1_HOST", 'localhost'),
                    "port": int(os.environ.get("TENANT_B_HOST1_PORT", 5021)),
                },
                "host2": {
                    "host": os.environ.get("TENANT_B_HOST2_HOST", 'localhost'),
                    "port": int(os.environ.get("TENANT_B_HOST2_PORT", 5022)),
                },
                "host3": {
                    "host": os.environ.get("TENANT_B_HOST3_HOST", 'localhost'),
                    "port": int(os.environ.get("TENANT_B_HOST3_PORT", 5023)),
                }
            },
            "nfv": {
                "host": os.environ.get("TENANT_B_NFV_HOST", 'localhost'),
                "port": int(os.environ.get("TENANT_B_NFV_PORT", 5029)),
            }
        }
    }
}

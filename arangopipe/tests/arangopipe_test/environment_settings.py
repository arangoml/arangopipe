from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix=False,
    load_dotenv=True,
    auto_cast=False,
    # settings_files=['settings.toml', '.secrets.toml'],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
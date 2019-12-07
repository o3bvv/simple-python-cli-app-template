Changelog
=========

{%- set version_title -%}
{{ cookiecutter.version }} ({% now 'local', '%b %d, %Y' %})
{%- endset %}

{{ version_title }}
{% for _ in version_title -%}-{%- endfor %}

* Initial version.

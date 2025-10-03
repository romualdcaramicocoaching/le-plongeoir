---
layout: page
title: Enfants & éducatif
permalink: /enfants/
---

{% assign posts = site.posts | where_exp: "p", "p.categories contains 'enfants'" %}
<ul>
{% for p in posts %}
  <li><a href="{{ p.url | relative_url }}">{{ p.title }}</a></li>
{% endfor %}
</ul>

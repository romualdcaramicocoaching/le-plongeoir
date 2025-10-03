---
layout: page
title: Guides & comparatifs
permalink: /guides/
---

{% assign posts = site.posts | where_exp: "p", "p.categories contains 'materiel'" %}
<ul>
{% for p in posts %}
  <li><a href="{{ p.url | relative_url }}">{{ p.title }}</a></li>
{% endfor %}
</ul>

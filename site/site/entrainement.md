---
layout: page
title: Entraînement & technique
permalink: /entrainement/
---

{% assign posts = site.posts | where_exp: "p", "p.categories contains 'entrainement'" %}
<ul>
{% for p in posts %}
  <li><a href="{{ p.url | relative_url }}">{{ p.title }}</a></li>
{% endfor %}
</ul>

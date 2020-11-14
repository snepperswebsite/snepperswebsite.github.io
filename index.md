---
layout: default
---
<div class="container main">
  <div class="row">
    <header>
      <div><center><h1>{{ site.title }}</h1></center></div>
      <center>
        <span class="big-ornament">
        <img src="/assets/sneppers-logo.png" alt="Logo van De Sneppers"  height="350">
        </span>
      </center>
    </header>
  </div>

  <div class="row">
    <div class="col-md-1"></div>
    <div class="col-md-8 offset-md-1">
    <div markdown="1">
        {% include hoofdpagina.md %}

  <h2>Inhoud</h2>
  <div class="row">
    <div class="col-md-1"></div>
    <div class="col-md-8 offset-md-1">
    
      {% assign categories = site.categories | sort %}
      {% for category in categories %}
      <h3>{{ category | first }}</h3>
      <p>{% for posts in category %}
        
        <!-- count how many non-hidden posts there are -->
        {% assign numvisibleposts = 0 %}
        {% for post in posts %}
            {% unless post.visible == 0 %}
                {% assign numvisibleposts = numvisibleposts | plus: 1 %}
            {% endunless %}
        {% endfor %}
        
        <!-- loop through all posts, show if not hidden, and don't add a comma if this is the last visible post -->
        {% assign postsplaced = 0 %}
        {% for post in posts %}
            {% if post.visible == 1 %}
                <a href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
                {% assign postsplaced = postsplaced | plus: 1 %}
                {% if postsplaced != numvisibleposts %}
                    ,&nbsp;&nbsp;
                {% endif %}
            {% endif %}
        {% endfor %}
        
      {% endfor %}</p>
      {% endfor %}
  </div>
</div>

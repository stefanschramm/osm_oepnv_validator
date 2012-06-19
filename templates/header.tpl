<%page args="profile,page" />
<h1>${profile['name'] | h}</h1>
<div class="menu menu-${page}">
<a href="${profile['shortname'] | h}.htm" class="menuentry-relations">Relations</a>
<a href="${profile['shortname'] | h}_lines.htm" class="menuentry-routes">Routes with stops</a>
</div>

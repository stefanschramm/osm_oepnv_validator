<div class="indexlink"><a href="index.htm">index</a></div>
<%page args="profile,page" />
<h1>${profile.label | h}</h1>
<div class="menu menu-${page}">
<a href="${profile.name | h}.htm" class="menuentry">Relations</a>
% if profile.stopplan:
<a href="${profile.name | h}_lines.htm" class="menuentry">Routes with stops</a>
% endif
% for map in profile.maps:
<a href="${profile.name}_map_${map | h}.htm" class="menuentry">Map: ${profile.maps[map][0] | h}</a>
% endfor
</div>

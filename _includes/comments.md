{% if site.duoshuo %}
	{% if page.thread %}
	<div class="ds-thread" data-thread-key="{{ page.thread }}" data-url="{{ site.url }}{{ page.url }}" data-title="{{ page.title }}" />
	{% else %}
	<div class="ds-thread" />
	{% endif %}	
	<script type="text/javascript">
	var duoshuoQuery = {short_name:"{{ site.duoshuo }}"};
	(function() {
		var ds = document.createElement('script');
		ds.type = 'text/javascript';ds.async = true;
		ds.src = 'http://static.duoshuo.com/embed.js';
		ds.charset = 'UTF-8';
		(document.getElementsByTagName('head')[0] 
		|| document.getElementsByTagName('body')[0]).appendChild(ds);
	})();
	</script>
{% endif %}

{% if site.disqus %}
<div id="disqus_thread"></div>
<script>
var disqus_config = function () {
    this.page.url = "{{ site.url }}{{ page.url }}"; // Replace PAGE_URL with your page's canonical URL variable

    // Replace PAGE_IDENTIFIER with your page's unique identifier variable
	{% if page.thread %}
    this.page.identifier = "{{ page.url }}_{{ page.thread }}"; 
	{% else %}
    this.page.identifier = "{{ page.url }}";
	{% endif %}	
};
(function() { // DON'T EDIT BELOW THIS LINE
var d = document, s = d.createElement('script');

s.src = '//haiiiiiyun.disqus.com/embed.js';

s.setAttribute('data-timestamp', +new Date());
(d.head || d.body).appendChild(s);
})();
</script>
<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript" rel="nofollow">comments powered by Disqus.</a></noscript>
{% endif %}


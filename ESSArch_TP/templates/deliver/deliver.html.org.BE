{% extends "admin/base_site.html" %}
{% load i18n %}
{% load staticfiles %}

{% block breadcrumbs %} 
{% endblock %} 

{% block content %} 

<div style="margin:20px">

<H1>Deliver information package for <i>({{ ip.label }})</i> from <i>({{ ip.archivist_organization }})</i></H1><p>
<p><i>Please fill in the fields or use prefilled data   (* indicates mandatory field)</i></p><br/>
 
<form action="/deliver/{{ip.id}}" method="post">
{% csrf_token %}
  
<table id="result_list">
	<thead> </thead>
	<tbody>
	  <tr>
      	    <td>Source Root</td>
      	    <td>{{ sourceroot }}</td>
          </tr>
          <tr>
            <td>Destination</td> 
            <td>{{ destination }}</td>
          </tr>
    	</tbody>
</table>
  
<br/>

    {#<tr><td>Source Root</td><td>{{ sourceroot }}</td></tr>#}
{#    <tr>#}
{#      <td>Destination</td>#} 
{#      <td>{{ form.destination }}</td>#}
{#      <td>{{ form.destination.errors }}</td>#}
{#    </tr>#}

  <br/>

  <input type="submit" value="Deliver" />
  </form>
</div>

{% endblock %} 

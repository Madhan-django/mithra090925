{% extends 'adminpanel/index.html' %}

{% block content %}

<div class="text-warning bg-dark"><h3 align="center">New Exam</h3></div><br><br>
  <div class="col-11">
      <br><br><br>
	  <div class="wlsm-form-section">
				<div class="row">

					<div class="col-md-6">
						<div class="wlsm-form-sub-heading wlsm-font-bold">Students Details</div>
						<li>
								<span class="wlsm-font-bold">Student Name :</span>
								<span>{{data.exam_stu}}</span>
						</li>
						<li>
								<span class="wlsm-font-bold">Father Name :</span>
								<span>{{data.exam_stu.father_name}}</span>
							</li>
						<li>
								<span class="wlsm-font-bold">Class:</span>
								<span>{{data.exam_label.exam_class}}</span>
							</li>

					</div>

					<div class="col-md-6">
						<div class="wlsm-form-sub-heading wlsm-font-bold">Exam Details</div>

						<ul class="wlsm-exam-details">

							<li>
								<span class="wlsm-font-bold">Exam Title:</span>
								<span>{{data.exam_label}}</span>
							</li>

							<li>
								<span class="wlsm-font-bold">Exam Center:</span>
								<span>{{data.exam_label.exam_centre}}</span>
							</li>
							<li>
								<span class="wlsm-font-bold">Start Date:</span>
								<span>{{data.exam_label.exam_start_date}}</span>
							</li>
							<li>
								<span class="wlsm-font-bold">End Date:</span>
								<span>{{data.exam_label.exam_end_date}}</span>
							</li>
						</ul>
					</div>
				</div>
			</div>
<form method="post">

  {% csrf_token %}
  {{ formset.management_form }}
	{% for form in formset %}
	<table style="border: 1px solid black;">
	{% for field in form %}
		<td width="350" style="border: 1px solid black ; padding: 15px;">{{field.label}} &nbsp;</td>
		<td width="350" style="border: 1px solid black ; padding: 15px;">{{field }} &nbsp;</td>
     {% endfor %}
		</table>
     <br>
	{% endfor %}
<input type="submit" value="Submit">

</form>
  </div>
{% endblock %}

# Load default config and override config from an environment variable
#app.config.update(dict(
#    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
#    DEBUG=True,
#    SECRET_KEY='development key',
#    USERNAME='admin',
#    PASSWORD='default'
#))
#app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def execqry(qry):
    output = Popen(['./runquery.sh', qry], stdout=PIPE).stdout.read()
    output=(re.sub(u'(?imu)^\s*\n', u'', output))[:-1]
    results = [dict(sym=i.split("\t")[0], var=i.split("\t")[1]) for i in output.split("\n")]
    return results


     dataPoints: [
{% for result in results %}
{ label: "{{ result.sym }}", y:{{ result.var }} },
{% endfor %}
    ]
   }
  ]
 }
);



------


<script type="text/javascript">
window.onload = function() {
 var chart = new CanvasJS.Chart("chartContainer",
  {
   title:{ text: "Volatility" },
   axisX: { gridColor: "Silver", tickColor: "silver" },
   toolTip: { shared:true },
   theme: "theme2",
   axisY: { gridColor: "Silver", tickColor: "silver", interlacedColor: "#F5F5F5" },
   legend: { verticalAlign: "center", horizontalAlign: "right" },
   data: [
{% for result in results %}
    {
      type: "line",
      showInLegend: true,
      lineThickness: 2,
      name: "{{ result.sym }}",
      color: "#"+((1<<24)*Math.random()|0).toString(16),
      dataPoints: [
{% for data in result.res %}
         { label: "{{ data.date }}", y: {{ data.val}} },
{% endfor %}
      ]
    },
{% endfor %}
   ] } );
chart.render();
}

</script>


{% if prevq != '' %}
<b> {{ prevq }} </b>:
<br><br>
<br>
<div id="chartContainer" style="height: 300px; width: 100%;"> </div>

{% endif %}


----------------------
Graph.css

path { 
    stroke: steelblue;
    stroke-width: 2;
    fill: none;
}

.axis path,
.axis line {
    fill: none;
    stroke: grey;
    stroke-width: 1;
    shape-rendering: crispEdges;
}

.legend {
    font-size: 16px;
    font-weight: bold;
    text-anchor: middle;
}


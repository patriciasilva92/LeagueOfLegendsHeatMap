// Carga los datos usando una petición AJAX
d3.json("ruta/a/datos.json", function(data) {
  // Crea un contenedor para la visualización
  var container = d3.select("#heatmap-container");

  // Crea una instancia del objeto d3-heatmap y configúralo
  var heatmap = d3.heatmap()
    .margin({ top: 50, right: 50, bottom: 50, left: 50 })
    .colorScale(["#FFFFCC", "#800026"])
    .cellSize(10)
    .numBins(20);

  // Enlaza los datos a la visualización
  var cells = container.selectAll(".cell")
    .data(data);

  // Crea las celdas rectangulares en la visualización
  cells.enter()
    .append("rect")
    .attr("class", "cell")
    .attr("x", function(d) { return heatmap.xScale(d.x); })
    .attr("y", function(d) { return heatmap.yScale(d.y); })
    .attr("width", heatmap.cellSize())
    .attr("height", heatmap.cellSize())
    .attr("fill", function(d) { return heatmap.colorScale()(d.value); });

  // Agrega interactividad a la visualización
  cells.on("mouseover", function(d) {
    // Actualiza la visualización al pasar el mouse sobre una celda
    d3.select(this).attr("fill", "#E31A1C");
  }).on("mouseout", function(d) {
    // Actualiza la visualización al quitar el mouse de una celda
    d3.select(this).attr("fill", function(d) { return heatmap.colorScale()(d.value); });
  });

  // Agrega la visualización al contenedor
  container.append("g")
    .attr("class", "heatmap")
    .call(

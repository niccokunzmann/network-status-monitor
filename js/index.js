
var names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

var colors = {
  "Mon" : "red",
  "Tue" : "green",
  "Wed" : "blue",
  "Thu" : "orange",
  "Fri" : "brown",
  "Sat" : "purple",
  "Sun" : "yellow",
};

function showDays(xValues, values) {
  var datasets = [];
  for (var i = 0; i < values.length; i++) {
        datasets.push({
        data: values[i],
        borderColor: colors[names[i]],
        fill: false
      });
  }
  new Chart("wholeDay", {
    type: "line",
    data: {
      labels: xValues,
      datasets: datasets,
    },
    options: {
      legend: {display: false},
      title: {
        display: true,
        text: "Internet Availability by Time in %"
      }
    }
  });
}


function showWeekOverview(yValues) {
  console.log("weekly" + JSON.stringify(yValues));
  var xValues = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
  var barColors = [colors.Mon, colors.Tue, colors.Wed, colors.Thu, colors.Fri, colors.Sat, colors.Sun];

  new Chart("weekOverview", {
    type: "doughnut",
    data: {
      labels: xValues,
      datasets: [{
        backgroundColor: barColors,
        data: yValues
      }]
    },
    options: {
      title: {
        display: true,
        text: "Weekly Overview of Internet Availability in %"
      }
    }
  });
}


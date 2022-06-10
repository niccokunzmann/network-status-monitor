
var colors = {
  "Mon" : "red",
  "Tue" : "green",
  "Wed" : "blue",
  "Thu" : "orange",
  "Fri" : "brown",
  "Sat" : "purple",
  "Sun" : "yellow",
};


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


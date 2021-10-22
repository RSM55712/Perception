function analyze() {
  var url = document.getElementById("url").value;

  fetch("http://api.perception.tk:8000", {
    method: "post",
    body: url
  }).then(response => {
    return response.json();
  }).then(data => {
    document.getElementById("content-text").classList.add("d-none");
    document.getElementById("loader").classList.remove("d-none");

    document.getElementById("title").innerText = data["title"];
    document.getElementById("authors").innerText = data["authors"];
    document.getElementById("publish_date").innerText = data["publish_date"];
    document.getElementById("sentiment").innerText = "Sentiment: " + data["sentiment"];
    document.getElementById("left").style.width = data["left"] * 100 + "%";
    document.getElementById("right").style.width = data["right"] * 100 + "%";

    var people = [];
    var organizations = [];

    for (const entity of data["entities"]) {
      if (entity["type"] === "person") {
        if (people.includes(entity["text"]))
          continue;

        if (people.length == 5)
          continue;

        people.push(entity["text"]);
      }
      else if (entity["type"] === "organization") {
        if (organizations.includes(entity["text"]))
          continue;

        if (organizations.length == 5)
          continue;

        organizations.push(entity["text"]);
      }
    }

    var entities = document.getElementById("entities");

    if (people.length > 0) {
      var ul = document.createElement("ul");
      var h4 = document.createElement("h4");
      h4.innerText = "People";
      entities.appendChild(h4);
      entities.appendChild(ul);

      for (const person of people) {
        var li = document.createElement("li");
        li.appendChild(document.createTextNode(person));
        ul.appendChild(li);
      }
    }

    if (organizations.length > 0) {
      var ul = document.createElement("ul");
      var h4 = document.createElement("h4");
      h4.innerText = "Organizations";
      entities.appendChild(h4);
      entities.appendChild(ul);

      for (const organization of organizations) {
        var li = document.createElement("li");
        li.appendChild(document.createTextNode(organization));
        ul.appendChild(li);
      }
    }

    if (people.length > 0 || organizations.length > 0) {
      document.getElementById("entities-separator").classList.remove("d-none");
    }

    document.getElementById("summary").innerText = data["summary"];

    document.getElementById("loader").classList.add("d-none");
    document.getElementById("content").classList.remove("d-none");
  }).catch(error => {
    var div = document.createElement("div");
    div.classList.add("alert", "alert-danger", "text-center");
    div.innerText = "An error occurred. Please try again later.";

    document.getElementById("loader").classList.add("d-none");
    document.getElementById("alerts").appendChild(div);
  });

  return false;
}

function analyzeText() {
  var text = document.getElementById("text").value;

  fetch("http://api.perception.tk:8000/text", {
    method: "post",
    body: text
  }).then(response => {
    return response.json();
  }).then(data => {
    document.getElementById("content").classList.add("d-none");
    document.getElementById("loader").classList.remove("d-none");

    document.getElementById("input-text").innerText = text;
    document.getElementById("left-text").style.width = data["left"] * 100 + "%";
    document.getElementById("right-text").style.width = data["right"] * 100 + "%";

    document.getElementById("loader").classList.add("d-none");
    document.getElementById("content-text").classList.remove("d-none");
  }).catch(error => {
    console.log(error);
    var div = document.createElement("div");
    div.classList.add("alert", "alert-danger", "text-center");
    div.innerText = "An error occurred. Please try again later.";

    document.getElementById("loader").classList.add("d-none");
    document.getElementById("alerts").appendChild(div);
  });

  return false;
}

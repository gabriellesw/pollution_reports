  let polluterSearch;
  let reporterSearch;
  let map;

  const addressComponents = {
    street_number: "short_name",
    route: "long_name",
    locality: "long_name",
    administrative_area_level_1: "long_name",
    administrative_area_level_2: "long_name",
    postal_code: "short_name",
  };

  function initAutocomplete() {
    initPolluterSearch();
    initReporterSearch();
  }

  function initPolluterSearch() {
    polluterSearch = new google.maps.places.Autocomplete(
      document.getElementById("polluter_search"),
      { types: ["geocode", "establishment"] }
    );
    polluterSearch.setFields([
        "address_component", "place_id", "formatted_address", "name", "geometry.location"
    ]);
    polluterSearch.setComponentRestrictions({"country": ["us"]});
    polluterSearch.addListener("place_changed", function () {autoFillAddress(true)});
  }

  function initReporterSearch() {
    reporterSearch = new google.maps.places.Autocomplete(
        document.getElementById("reporter_search"),
        {types: ["geocode"]}
    );
    reporterSearch.setFields([
        "address_component", "formatted_address", "geometry.location"
    ])
    reporterSearch.setComponentRestrictions({"country": ["us"]});
    reporterSearch.addListener("place_changed", function () {autoFillAddress(false)});
  }

  function autoFillAddress(polluter=false) {
    var place;
    var prefix;
    if(polluter === true) {
      place = polluterSearch.getPlace();
      document.getElementById("polluter_name").value = place.name;
      prefix = "polluter_";
    }

    else {
      place = reporterSearch.getPlace();
      prefix = "";
    }

    document.getElementById(prefix + "lat").value = place.geometry.location.lat();
    document.getElementById(prefix + "lng").value = place.geometry.location.lng();

    for (const component of place.address_components) {
      const addressType = component.types[0];

      if (addressComponents[addressType]) {
        document.getElementById(prefix + addressType).value = component[addressComponents[addressType]];
      }
    }

    let fullAddress = document.getElementById(prefix + "address");
    let streetNumber = document.getElementById(prefix + "street_number");
    let route = document.getElementById(prefix + "route");
    fullAddress.value = streetNumber.value + " " + route.value;

    if(polluter === true) {

      map.setCenter(place.geometry.location);
      map.setZoom(15);

      const marker = new google.maps.Marker({
        map,
        position: place.geometry.location,
        title: place.name,
      });
      const infowindow = new google.maps.InfoWindow(
          {content: "<b>Location: </b>" + place.name + "<br><b>Address: </b>" + place.formatted_address}
      );
      infowindow.open(map, marker);
    }
  }

  function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
      // Hardcoded State of California
      center: { lat: 36.778261, lng: -119.4179324 },
      zoom: 6,
    });
  }

  function geolocate(polluter= false) {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        const geolocation = {
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        };
        const circle = new google.maps.Circle({
          center: geolocation,
          radius: position.coords.accuracy,
        });
        if(polluter === true) {
          polluterSearch.setBounds(circle.getBounds());
          if (document.getElementById("polluter_lat").value === "") {
            map.setCenter(geolocation);
            map.setZoom(10);
          }
        }
        else {
          reporterSearch.setBounds(circle.getBounds());
        }
      });
    }
  }
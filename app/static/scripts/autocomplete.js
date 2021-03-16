  let polluterSearch;
  let map;
  const addressComponents = {
    street_number: "short_name",
    route: "short_name",
    locality: "long_name",
    administrative_area_level_1: "short_name",
    postal_code: "short_name",
  };

  function initPolluterSearch() {
    polluterSearch = new google.maps.places.Autocomplete(
      document.getElementById("polluter_search"),
      { types: ["geocode", "establishment"] }
    );
    polluterSearch.setFields([
        "address_component", "place_id", "formatted_address", "name", "geometry.location"
    ]);
    polluterSearch.setComponentRestrictions({"country": ["us"]})
    polluterSearch.addListener("place_changed", autoFillAddress);
  }

  function autoFillAddress() {
    const place = polluterSearch.getPlace();

    document.getElementById("lat").value = place.geometry.location.lat();
    document.getElementById("lng").value = place.geometry.location.lng();

    for (const component of place.address_components) {
      const addressType = component.types[0];

      if (addressComponents[addressType]) {
        const val = component[addressComponents[addressType]];
        document.getElementById(addressType).value = val;
      }
    }
    map.setCenter(place.geometry.location);
    map.setZoom(15);

    const marker = new google.maps.Marker({
      map,
      position: place.geometry.location,
      title: place.name,
    });
    const infowindow = new google.maps.InfoWindow(
        {content: "<b>Polluter: </b>" + place.name + "<br><b>Address: </b>" + place.formatted_address}
    );
    infowindow.open(map, marker);
  }

  function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
      // Hardcoded State of California
      center: { lat: 36.778261, lng: -119.4179324 },
      zoom: 6,
    });
  }

  function geolocate() {
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
        polluterSearch.setBounds(circle.getBounds());
        if (document.getElementById("lat").value === "") {
          map.setCenter(geolocation);
          map.setZoom(10);
        }
      });
    }
  }
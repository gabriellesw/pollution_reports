
  const addressComponents = {
    street_number: "short_name",
    route: "short_name",
    locality: "long_name",
    administrative_area_level_1: "short_name",
    postal_code: "short_name",
  };

  const geoComponents = ["lat", "lng"];

  function initPolluterSearch() {
    polluterSearch = new google.maps.places.Autocomplete(
      document.getElementById("polluter_search"),
      { types: ["geocode", "establishment"] }
    );
    polluterSearch.setFields(["address_component", "geometry.location"]);
    polluterSearch.setComponentRestrictions({"country": ["us"]})
    polluterSearch.addListener("place_changed", autoFillAddress);
  }

  function autoFillAddress() {
    const place = polluterSearch.getPlace();

    document.getElementById("lat").value = place.geometry.location.lat()
    document.getElementById("lng").value = place.geometry.location.lng()

    for (const component of place.address_components) {
      const addressType = component.types[0];

      if (addressComponents[addressType]) {
        const val = component[addressComponents[addressType]];
        document.getElementById(addressType).value = val;
      }
    }
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
      });
    }
  }

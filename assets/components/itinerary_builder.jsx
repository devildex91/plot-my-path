import React from "react";
import { useState } from "react";

function ItineraryBuilder({trip, preferences, days, attractions}){


const startDate = new Date(trip.start_date);
    const endDate = new Date(trip.end_date);

    const tripLength = Math.round(
        (endDate - startDate) / (1000 * 60 * 60 * 24)
    )


 
 return(
<>
<div className="tabs tabs-box">
  <input type="radio" name="my_tabs_6" className="tab" aria-label="Itinerary" />
  <div className="tab-content bg-base-100 border-base-300 p-6">
 <p>
    Holiday length:{tripLength}


 </p>

  </div>

  <input type="radio" name="my_tabs_6" className="tab" aria-label="Map" defaultChecked />
  <div className="tab-content bg-base-100 border-base-300 p-6">Tab content 2</div>

  <input type="radio" name="my_tabs_6" className="tab" aria-label="Weather" />
  <div className="tab-content bg-base-100 border-base-300 p-6">Tab content 3</div>
</div>
</>

 )

}

export default ItineraryBuilder  
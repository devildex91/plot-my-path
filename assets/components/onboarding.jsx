import React, { useState } from 'react';

function Onboarding({homeUrl}) {
  const staticUrl = window.DJANGO_STATIC_URL || '/static/';
  

  return (
    
    <div className="flex flex-col min-h-screen justify-between items-center bg-base-100 p-6 text-primary ">
      <div className="flex flex-row w-full max-w-5xl items-center mb-6">
    <h1 className = " card-title text-5xl font-bold"> What we do</h1>
    <a href={homeUrl} className="btn btn-primary w-fit ml-auto rounded-xl">skip</a>
    </div>
    <div className="carousel w-full flex-grow max-w-5xl">

  <div id="item1" className="carousel-item w-full">
    <div className="card bg-base-200 w-full shadow-sm animate-fade-in shadow-sm animate-fade-in flex flex-col  p-6 items-center gap-6">
      
            <figure className="w-full md:w-1/2 flex justify-center">
              <img
                src={`${staticUrl}images/personalised_itinery.avif`}
                alt="Items on table while planning for a trip"
                className="rounded-xl object-cover h-auto w-3/4 sm:w-1/2 md:w-full"
              />
            </figure>
            <div className="card-body items-center text-center grow-0 ">
              <h2 className="card-title text-4xl font-bold">Personalised Itineraries</h2>
              <p className="text-xl text-center mx-2 my-4 opacity-80">
                Tell us your preferences and we will create the perfect trip just for you.
              </p>
            </div>
            <a href="#item2" className="btn btn-primary rounded-xl mx-2 mb-2 md:mb-6 w-full sm:w-1/2 self-center">Next</a>
          </div>
  </div>
  <div id="item2" className="carousel-item w-full relative">
    <div className="card bg-base-200 w-full shadow-sm animate-fade-in flex flex-col p-6 items-center gap-6">
        <a href="#item1" className="btn btn-primary w-fit rounded-xl absolute top-4 left-4 z-10">❮</a>
            <figure className="w-full md:w-1/2 flex justify-center pt-10 md:pt-0">
              <img
                src={`${staticUrl}images/new_discovery.avif`}
                alt="A person discovering new places"
                className="rounded-xl object-cover h-auto w-3/4 sm:w-1/2 md:w-full"
              />
            </figure>
            <div className="card-body items-center text-center grow-0">
              <h2 className="card-title text-4xl font-bold">Discover Amazing Destinations</h2>
              <p className="text-xl text-center mx-2 opacity-80">
                Explore top attractions, hidden gems and local favourites.
              </p>
            </div>
            <a href="#item3" className="btn btn-primary rounded-xl mx-2 mb-2 md:mb-6 w-full sm:w-1/2 self-center">Next</a>
          </div>
  </div>
  <div id="item3" className="carousel-item w-full relative">
  <div className="card bg-base-200 w-full shadow-sm animate-fade-in flex flex-col p-6 items-center gap-6">
    <a href="#item2" className="btn btn-primary w-fit absolute top-4 left-4 z-10">❮</a>
            <figure className="w-full md:w-1/2 flex justify-center pt-10 md:pt-0">
              <img
                src={`${staticUrl}images/real_time.avif`}
                alt="Real time data being used to plan a trip"
                className="rounded-xl object-cover h-auto w-3/4 sm:w-1/2 md:w-full"
              />
            </figure>
            <div className="card-body items-center text-center grow-0">
              <h2 className="card-title text-4xl font-bold mb-4">Real-Time Info</h2>
              <p className="text-xl text-center mx-2 opacity-80">
                Get live weather updates, travel tips and smart recommendations.
              </p>
            </div>
            <a href={homeUrl} className="btn btn-primary rounded-xl mx-2 mb-2 md:mb-6 w-full sm:w-1/2 self-center">Get Started</a>
          </div>
  </div>
  
</div>
</div>

  );
}

export default Onboarding;

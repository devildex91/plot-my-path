import React, { useState } from 'react';

function Onboarding({homeUrl}) {
  const staticUrl = window.DJANGO_STATIC_URL || '/static/';
  

  return (
    <div className="flex flex-col min-h-screen justify-between items-center bg-base-100 p-6 text-primary ">
    <h1 className = " card-title text-5xl self-center font-bold mb-2"> What we do</h1>
    <div className="carousel w-full flex-grow">
  <div id="item1" className="carousel-item w-full">
    <div className="card bg-base-200 w-full shadow-sm animate-fade-in">
        <a href={homeUrl} className="btn btn-primary w-fit mr-2 mt-2 ml-auto rounded-xl">skip</a>
            <figure className="px-10 pt-10">
              <img
                src={`${staticUrl}images/personalised_itinery.avif`}
                alt="Items on table while planning for a trip"
                className="rounded-xl object-cover h-auto w-full sm:max-w-3/4 md:max-w-1/2"
              />
            </figure>
            <div className="card-body items-center text-center">
              <h2 className="card-title text-4xl font-bold">Personalised Itineraries</h2>
              <p className="text-xl text-center mx-2 my-4 opacity-80">
                Tell us your preferences and we will create the perfect trip just for you.
              </p>
            </div>
            <a href="#item2" className="btn btn-primary rounded-xl mx-2 mb-2 w-full sm:w-1/2 self-center">Next</a>
          </div>
  </div>
  <div id="item2" className="carousel-item w-full">
    <div className="card bg-base-100 w-full shadow-sm animate-fade-in">
        <a href="#item1" className="btn btn-primary w-fit rounded-xl">❮</a>
            <figure className="px-10 pt-10">
              <img
                src={`${staticUrl}images/new_discovery.avif`}
                alt="A person discovering new places"
                className="rounded-xl object-cover h-auto w-full sm:max-w-3/4 md:max-w-1/2"
              />
            </figure>
            <div className="card-body items-center text-center">
              <h2 className="card-title text-4xl font-bold">Discover Amazing Destinations</h2>
              <p className="text-xl text-center mx-2 opacity-80">
                Explore top attractions, hidden gems and local favourites.
              </p>
            </div>
            <a href="#item3" className="btn btn-primary rounded-xl w-full sm:w-1/2 self-center">Next</a>
          </div>
  </div>
  <div id="item3" className="carousel-item w-full">
  <div className="card bg-base-100 w-full shadow-sm animate-fade-in">
    <a href="#item2" className="btn btn-primary w-fit">❮</a>
            <figure className="px-10 pt-10 mb-4">
              <img
                src={`${staticUrl}images/real_time.avif`}
                alt="Real time data being used to plan a trip"
                className="rounded-xl object-cover h-auto w-full sm:max-w-3/4 md:max-w-1/2"
              />
            </figure>
            <div className="card-body items-center text-center">
              <h2 className="card-title text-4xl font-bold mb-4">Real-Time Info</h2>
              <p className="text-xl text-center mx-2 opacity-80">
                Get live weather updates, travel tips and smart recommendations.
              </p>
            </div>
            <a href={homeUrl} className="btn btn-primary rounded-xl w-full sm:w-1/2 self-center">Get Started</a>
          </div>
  </div>
  
</div>
</div>
  );
}

export default Onboarding;

from ..api.data import Data

def cars():  # pragma: no cover (as this data is like any other data)
    return Data([
        {"model": "leon", "motor": "electric", "color": "red", "doors": 5, "sales": 10},
        {"model": "ibiza", "motor": "electric", "color": "white", "doors": 3, "sales": 15},
        {"model": "cordoba", "motor": "diesel", "color": "black", "doors": 5, "sales": 3},
        {"model": "toledo", "motor": "diesel", "color": "white", "doors": 5, "sales": 18},
        {"model": "altea", "motor": "diesel", "color": "red", "doors": 5, "sales": 4},
        {"model": "arosa", "motor": "electric", "color": "red", "doors": 3, "sales": 12},
        {"model": "alhambra", "motor": "diesel", "color": "white", "doors": 5, "sales": 5},
        {"model": "600", "motor": "gasoline", "color": "yellow", "doors": 3, "sales": 20},
        {"model": "127", "motor": "gasoline", "color": "white", "doors": 5, "sales": 2},
        {"model": "panda", "motor": "gasoline", "color": "black", "doors": 3, "sales": 13}
    ])

def energy():  # pragma: no cover (as this data is like any other data)
    return Data([
        {"source": "wind", "region": "north", "month": "jan", "production": 700, "cost": 60},
        {"source": "hydro", "region": "west", "month": "jan", "production": 800, "cost": 55},
        {"source": "solar", "region": "south", "month": "jan", "production": 500, "cost": 50},

        {"source": "solar", "region": "north", "month": "feb", "production": 450, "cost": 55},
        {"source": "hydro", "region": "north", "month": "feb", "production": 780, "cost": 57},
        {"source": "wind", "region": "south", "month": "feb", "production": 650, "cost": 58},

        {"source": "wind", "region": "east", "month": "mar", "production": 720, "cost": 62},
        {"source": "hydro", "region": "south", "month": "mar", "production": 820, "cost": 59},
        {"source": "solar", "region": "east", "month": "mar", "production": 480, "cost": 53},

        {"source": "wind", "region": "west", "month": "apr", "production": 750, "cost": 65},
        {"source": "solar", "region": "west", "month": "apr", "production": 520, "cost": 51},
        {"source": "hydro", "region": "east", "month": "apr", "production": 900, "cost": 60}
    ])

def hotels():  # pragma: no cover (as this data is like any other data)
    return Data([
        {"city": "valencia", "type": "hotel", "rooms": 100, "occupancy": 0.82, "price": 130},
        {"city": "madrid", "type": "hotel", "rooms": 120, "occupancy": 0.80, "price": 140},
        {"city": "sevilla", "type": "hotel", "rooms": 80, "occupancy": 0.80, "price": 100},
        {"city": "barcelona", "type": "hotel", "rooms": 130, "occupancy": 0.78, "price": 150},
        {"city": "madrid", "type": "hostel", "rooms": 50, "occupancy": 0.65, "price": 60},
        {"city": "valencia", "type": "hostel", "rooms": 40, "occupancy": 0.60, "price": 55},
        {"city": "barcelona", "type": "hostel", "rooms": 70, "occupancy": 0.72, "price": 75},
        {"city": "madrid", "type": "hotel", "rooms": 100, "occupancy": 0.75, "price": 120},
        {"city": "barcelona", "type": "hotel", "rooms": 150, "occupancy": 0.85, "price": 160},
        {"city": "valencia", "type": "hotel", "rooms": 90, "occupancy": 0.78, "price": 110},
        {"city": "sevilla", "type": "hostel", "rooms": 35, "occupancy": 0.70, "price": 50}
    ])

def orders():  # pragma: no cover (as this data is like any other data)
    return Data([
        {"customer": "c2", "country": "fr", "status": "cancelled", "total": 60},
        {"customer": "c1", "country": "es", "status": "delivered", "total": 140},
        {"customer": "c3", "country": "fr", "status": "pending", "total": 90},
        {"customer": "c4", "country": "de", "status": "processing", "total": 110},
        {"customer": "c2", "country": "fr", "status": "delivered", "total": 200},
        {"customer": "c1", "country": "es", "status": "pending", "total": 80},
        {"customer": "c3", "country": "fr", "status": "delivered", "total": 150},
        {"customer": "c4", "country": "de", "status": "returned", "total": 50},
        {"customer": "c1", "country": "es", "status": "delivered", "total": 120}
    ])

def retail():  # pragma: no cover (as this data is like any other data)
    return Data([
        {"store": "s4", "product": "shirt", "category": "clothing", "units": 15, "revenue": 450},
        {"store": "s1", "product": "phone", "category": "tech", "units": 8, "revenue": 6400},
        {"store": "s3", "product": "desk", "category": "home", "units": 4, "revenue": 1200},
        {"store": "s2", "product": "chair", "category": "home", "units": 10, "revenue": 1500},
        {"store": "s1", "product": "chair", "category": "home", "units": 7, "revenue": 1050},
        {"store": "s4", "product": "shoes", "category": "clothing", "units": 10, "revenue": 600},
        {"store": "s3", "product": "phone", "category": "tech", "units": 6, "revenue": 4800},
        {"store": "s2", "product": "laptop", "category": "tech", "units": 3, "revenue": 3000},
        {"store": "s1", "product": "laptop", "category": "tech", "units": 5, "revenue": 5000}
    ])

def usage():  # pragma: no cover (as this data is like any other data)
    return Data([
        {"user": "u3", "platform": "ios", "country": "es", "minutes": 20},
        {"user": "u2", "platform": "android", "country": "fr", "minutes": 40},
        {"user": "u5", "platform": "ios", "country": "it", "minutes": 50},
        {"user": "u1", "platform": "ios", "country": "es", "minutes": 25},
        {"user": "u4", "platform": "web", "country": "de", "minutes": 200},
        {"user": "u3", "platform": "android", "country": "fr", "minutes": 15},
        {"user": "u2", "platform": "android", "country": "fr", "minutes": 35},
        {"user": "u1", "platform": "ios", "country": "es", "minutes": 30}
    ])


def calculate_savings_per_mile(gasoline_price, mpg, electricity_cost, ev_efficiency):
    fuel_cost_per_mile = gasoline_price / mpg
    ev_cost_per_mile = electricity_cost / ev_efficiency 
    return fuel_cost_per_mile - ev_cost_per_mile

gasoline_price = 3.00  
mpg = 25  
electricity_cost = 0.12  
ev_efficiency = 0.3  

savings_per_mile = calculate_savings_per_mile(gasoline_price, mpg, electricity_cost, ev_efficiency)
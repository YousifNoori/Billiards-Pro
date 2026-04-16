#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "phylib.h"
#include <math.h>

phylib_object *phylib_new_still_ball( unsigned char number, phylib_coord *pos ){
    phylib_object * object = (phylib_object *)calloc(1,sizeof(phylib_object)); // allocate memory for a new phylib_object
    if(object == NULL){ // CHecks if mem allocation failed
        return NULL; 
    }

    object->type = PHYLIB_STILL_BALL; // set its type to PHYLIB_STILL_BALL and transfer paramters into structure
    object->obj.still_ball.number = number;
    object->obj.still_ball.pos = *pos;

    return object; // Returns the created object
}

phylib_object *phylib_new_rolling_ball( unsigned char number,
phylib_coord *pos,
phylib_coord *vel,
phylib_coord *acc ){

    phylib_object * object = (phylib_object *)calloc(1,sizeof(phylib_object)); // allocate memmory for a new phylib_object 

    if(object == NULL){ // CHecks if mem allocation failed
        return NULL; 
    }
    
    object->type = PHYLIB_ROLLING_BALL; // set type to rolling ball and transfers paramters into structure

    object->obj.rolling_ball.number = number;
    object->obj.rolling_ball.pos = *pos;
    object->obj.rolling_ball.vel = *vel;
    object->obj.rolling_ball.acc = *acc;

    return object; // Returns the created object

}

phylib_object *phylib_new_hole( phylib_coord *pos ){

    phylib_object * object = (phylib_object *)calloc(1,sizeof(phylib_object)); // allocate memmory for a new phylib_object

    if(object == NULL){ // CHecks if mem allocation failed
        return NULL; 
    }

    object->type = PHYLIB_HOLE; // sets type to a hole and transfers the holes position into structure
    object->obj.hole.pos = *pos;

    return object; // Returns the created object

}

phylib_object *phylib_new_hcushion( double y ){
    
    phylib_object * object = (phylib_object *)calloc(1,sizeof(phylib_object)); // allocate memmory for a new phylib_object 

    if(object == NULL){ // CHecks if mem allocation failed
        return NULL; 
    }

    object->type = PHYLIB_HCUSHION; // sets type to a hcushion and transfers position into structure    
    object->obj.hcushion.y = y;

    return object; // returns new object created
}

phylib_object *phylib_new_vcushion( double x ){
    
    phylib_object * object = (phylib_object *)calloc(1,sizeof(phylib_object)); // allocate memmory for a new phylib_object 

    if(object == NULL){ // CHecks if mem allocation failed
        return NULL; 
    }

    object->type = PHYLIB_VCUSHION; // sets type to a vcushion and transfers position into stucture
    object->obj.vcushion.x = x;

    return object; // returns new object created created


}

phylib_table *phylib_new_table( void ){

    phylib_table * table = (phylib_table *)calloc(1,sizeof(phylib_table)); // allocate memmory for object 

    if(table == NULL){
        return NULL;
    }

    table->time = 0.0; // sets time to 0

    table->object[0] = phylib_new_hcushion(0.0); // Populates the table with new objects
    table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    table->object[2] = phylib_new_vcushion(0.0);
    table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);    
    table->object[4] = phylib_new_hole(&(phylib_coord){0.0,0.0});
    table->object[5] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_LENGTH});
    table->object[6] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_LENGTH / 2.0});
    table->object[7] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, 0});
    table->object[8] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH / 2.0});
    table->object[9] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH});


    for(int i = 10; i < PHYLIB_MAX_OBJECTS; i++){ // sets the remaining objects to NULL
        table->object[i] = NULL;
    }

    return table; // returns table
}

void phylib_copy_object( phylib_object **dest, phylib_object **src ){

    *dest = (phylib_object *)calloc(1,sizeof (phylib_object)); // allocates memmory of size phylib_object to *dest
    if(*src != NULL){ // checks if memm allocation worked
        memcpy(*dest, *src, sizeof(phylib_object)); // copys memmory from *src to *dest
    }else{
        *dest = NULL; // if mem allocation failed set dest to null
    }

}

phylib_table *phylib_copy_table( phylib_table *table ){

    phylib_table * newTable = (phylib_table *)calloc(1,sizeof(phylib_table)); // allocate memmory for a new phylib_table
    if(newTable == NULL){// check for memm allocation 
        return NULL;
    }
    newTable->time = table->time; // copies time to newTable
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){ // For loop to iterate through all the objects
        if(table->object[i] != NULL){ // checks to see if the object at index i is not null (a object)
            phylib_copy_object(&newTable->object[i], &table->object[i]); // Copies object to new table
        }else{
            newTable->object[i] = NULL; // If the object in the old table is null then set the object at that index in the newtable to null

        }
    }

    return newTable; // returns the copied table

}

void phylib_add_object( phylib_table *table, phylib_object *object ){ 

    int i = 0; // counter variable
    while(table->object[i] != NULL && i < PHYLIB_MAX_OBJECTS){ // counts how many objects are currently in the loop
        i++; 
    }

    if(table->object[i] == NULL && i < PHYLIB_MAX_OBJECTS){ // checks if there is room to add a new object
        table->object[i] = object; // adds new object if theres room
    }
}

void phylib_free_table( phylib_table *table ){

    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){ // for loop to check the contents of the table
        if(table->object[i] != NULL){ // checks if the object pointed to contains an object
            free(table->object[i]); // frees that memmory
            table->object[i] = NULL; // sets it to null
        }
    }  
    free(table);  // frees the memmory stored in table
}

phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ){
    phylib_coord calculation; // creates a new coordinate to store the result of the operation
    calculation.x = c1.x - c2.x; // subratcts c2 from c1 for x and stores it in calculation.x
    calculation.y = c1.y - c2.y; // subratcts c2 from c1 for y and stores it in calculation.y
    return calculation; // returns the calculation


}

double phylib_length( phylib_coord c ){ 
    double calculation; // creats a new coordinate to store the result of the operation
    calculation = sqrt((c.x * c.x) + (c.y * c.y)); // uses Pythagorean theorem to calculate the length
    return calculation; // returns the calculation
}

double phylib_dot_product( phylib_coord a, phylib_coord b ){
    double calculation; // creates a new coordinate to store the result of the operation
    calculation = ((a.x * b.x) + (a.y * b.y)); // calculates the dot product and stores it in calculation
    return calculation; // returns calculation
}

double phylib_distance( phylib_object *obj1, phylib_object *obj2 ){
    if(obj1->type != PHYLIB_ROLLING_BALL){ // checks to see if obj1 is not a rolling ball
        return -1.0; // if it is not return -1.0
    }

    double distance = 0.0; // creates a variable to hold the distance calculated

    if(obj2->type == PHYLIB_ROLLING_BALL || obj2->type == PHYLIB_STILL_BALL){ // checks to see if obj 2 is another ball
        phylib_coord coords = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos); // calculates the distance between the 2 balls
        distance = phylib_length(coords) - PHYLIB_BALL_DIAMETER; // calculates the length subtracts 2 radii and stores it in distance
    }else if(obj2->type == PHYLIB_HOLE){ // checks to see if obj 2 is a hole
        phylib_coord coords = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos); // calculates the distance between the ball and the hole
        distance = phylib_length(coords) - PHYLIB_HOLE_RADIUS; // calculates the length and subtracts hole radius
    }else if(obj2->type == PHYLIB_HCUSHION){ // checks to see if obj 2 is a hcushion
        distance = fabs(obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS; // calculates the distance between the ball and cushion
    }else if(obj2->type == PHYLIB_VCUSHION){ // checks to see if obj 2 is a vcushion
        distance = fabs(obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS; // calculates the distance between the ball and cushion
    }else{
        distance = -1.0; // invalid type sets to -1.0
    }

    return distance; // returns distance;
}

void phylib_roll( phylib_object *new, phylib_object *old, double time ){

    if(new->type == PHYLIB_ROLLING_BALL && old->type == PHYLIB_ROLLING_BALL){ // checks to see if new and old are rolling balls
    
        double newPosX, newPosY, newVelX, newVelY; // declares new variables for positions and velecotiy   
        
        
        if(new->type == PHYLIB_ROLLING_BALL && old->type == PHYLIB_ROLLING_BALL){
            newPosX = old->obj.rolling_ball.pos.x + old->obj.rolling_ball.vel.x * time + 0.500000 * old->obj.rolling_ball.acc.x * (time * time);
            newPosY = old->obj.rolling_ball.pos.y + old->obj.rolling_ball.vel.y * time + 0.500000 * old->obj.rolling_ball.acc.y * (time * time);

            newVelX = old->obj.rolling_ball.vel.x + (old->obj.rolling_ball.acc.x * time);
            newVelY = old->obj.rolling_ball.vel.y + (old->obj.rolling_ball.acc.y * time);
            // calculates the new balls positions and velecoties using the old balls information

            new->obj.rolling_ball.pos.x = newPosX; // sets the position of the new ball to the calculated values
            new->obj.rolling_ball.pos.y = newPosY; 



            if((newVelX * old->obj.rolling_ball.vel.x) < 0){ // checks to see if velecoty changed sign
                new->obj.rolling_ball.vel.x = 0.0; // if so sets vel and acc to 0
                new->obj.rolling_ball.acc.x = 0.0;
            }else{
                new->obj.rolling_ball.vel.x = newVelX; // otherwise sets vel to the calculated vel
            }


            if((newVelY * old->obj.rolling_ball.vel.y) < 0){ // checks to see if vel changed sign
                new->obj.rolling_ball.vel.y = 0.0; // if so set vel and acc to 0
                new->obj.rolling_ball.acc.y = 0.0;    
            }else{
                new->obj.rolling_ball.vel.y = newVelY; // otherwise set vel to calculated vel
            }
        }
    }
}


unsigned char phylib_stopped( phylib_object *object ){

    double speed = phylib_length(object->obj.rolling_ball.vel); // calculates the speed of the ball  

    if(speed < PHYLIB_VEL_EPSILON){ // checks if the ball has stopped
        phylib_coord pos = object->obj.rolling_ball.pos; // takes position and number
        unsigned char number = object->obj.rolling_ball.number;
        object->type = PHYLIB_STILL_BALL; // makes it a still ball
        object->obj.still_ball.number = number; // transfers position and number
        object->obj.still_ball.pos = pos;
        return 1; // returns 1 for ball converted
    }
    return 0; // returns 0 for no ball converted
}

void phylib_bounce( phylib_object **a, phylib_object **b ){

    phylib_object *objectA = *a, *objectB = *b; // creates pointers to point to the pointers of the objects

    if(objectB->type == PHYLIB_HCUSHION){ // checks if object b is a hcushion : case 1
        objectA->obj.rolling_ball.vel.y = -(objectA->obj.rolling_ball.vel.y); // reverse y vel and acc
        objectA->obj.rolling_ball.acc.y = -(objectA->obj.rolling_ball.acc.y);
    }else if(objectB->type == PHYLIB_VCUSHION){ // checks if object b is a vcushion : case 2
        objectA->obj.rolling_ball.vel.x = -(objectA->obj.rolling_ball.vel.x); // reverse x vel and acc
        objectA->obj.rolling_ball.acc.x = -(objectA->obj.rolling_ball.acc.x);        
    }else if(objectB->type == PHYLIB_HOLE){ // checks if object b is a hole : case 3 
        free(*a); // frees memmory in a
        *a = NULL; // sets its pointer to null
    }else if(objectB->type == PHYLIB_STILL_BALL || objectB->type == PHYLIB_ROLLING_BALL){ // checks if object b is a ball : case 4 / 5
        if(objectB->type == PHYLIB_STILL_BALL){ // case 4 still ball
            objectB->type = PHYLIB_ROLLING_BALL;
        }
        // case 5 rolling ball
        phylib_coord r_ab = phylib_sub(objectA->obj.rolling_ball.pos, objectB->obj.rolling_ball.pos); // compute position of a
        phylib_coord v_rel = phylib_sub(objectA->obj.rolling_ball.vel, objectB->obj.rolling_ball.vel); // compute reltive vel

        double length = phylib_length(r_ab); 

        phylib_coord n; // normal vector
        n.x = r_ab.x / length; // calculate normal vector
        n.y = r_ab.y / length;

        double v_rel_n = phylib_dot_product(v_rel, n); // calculate ratio of relative vel

        objectA->obj.rolling_ball.vel.x -= v_rel_n * n.x; // update x and y vel for obj a
        objectA->obj.rolling_ball.vel.y -= v_rel_n * n.y;

        objectB->obj.rolling_ball.vel.x += v_rel_n * n.x; // update x and y vel for obj b
        objectB->obj.rolling_ball.vel.y += v_rel_n * n.y;

        double speedA, speedB; 
        speedA = phylib_length(objectA->obj.rolling_ball.vel); // calculates the speeds of both balls
        speedB = phylib_length(objectB->obj.rolling_ball.vel);

        if(speedA > PHYLIB_VEL_EPSILON){ // checks if speed is greater then vel epsilon
            objectA->obj.rolling_ball.acc.x = (-objectA->obj.rolling_ball.vel.x / speedA) * PHYLIB_DRAG; // change acc
            objectA->obj.rolling_ball.acc.y = (-objectA->obj.rolling_ball.vel.y / speedA) * PHYLIB_DRAG;
        }

        if(speedB > PHYLIB_VEL_EPSILON){ // check if speed is greater then vel epsilon
            objectB->obj.rolling_ball.acc.x = (-objectB->obj.rolling_ball.vel.x / speedB) * PHYLIB_DRAG; // change acc 
            objectB->obj.rolling_ball.acc.y = (-objectB->obj.rolling_ball.vel.y / speedB) * PHYLIB_DRAG;
        }
    }  
}

unsigned char phylib_rolling( phylib_table *t ){
    unsigned char count = 0; // counter for number of rolling balls
    if(t == NULL){ // if table is null returns 0
        return count;
    }

    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){ // iterates through the table
        if(t->object[i] != NULL){ // checks if an object exists
            if(t->object[i]->type == PHYLIB_ROLLING_BALL){ // checks if the object is a rolling ball
                count++; // increments counter
            }
        }
    }
    return count; // returns counter
}

phylib_table *phylib_segment(phylib_table *table) {



    int numRollingBalls = phylib_rolling(table); // gets the number of rolling balls
        


    if(numRollingBalls == 0){ // if there are no rolling balls returns null
        //phylib_free_table(table);
        return NULL;
    }
    
    phylib_table *newTable = phylib_copy_table(table); // copies the table to newTable
    double time = PHYLIB_SIM_RATE; // creates time variable
    int killLoop = 0; // creates killLoop switch

    while(time < PHYLIB_MAX_TIME && !killLoop){ // while loop to iterate while max time is not reached andno ball has stopped rolling
        for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){ // for loop to iterate through each object
            if(newTable->object[i] != NULL && newTable->object[i]->type == PHYLIB_ROLLING_BALL){ // checks to make sure rolling ball exist
                phylib_roll(newTable->object[i], table->object[i], time); // rolls the ball sending it new ball old ball and time
            }
        }

        for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){ // for loop to iterate through each object
            if(newTable->object[i] != NULL && newTable->object[i]->type == PHYLIB_ROLLING_BALL){ // checks to make sure rolling ball exist
                for(int j = 0; j < PHYLIB_MAX_OBJECTS; j++){ // for loop to iterate through each object
                    if(newTable->object[j] != NULL && j != i){ // checks to make sure the object exists and is not the same as the ball
                        if(phylib_distance(newTable->object[i], newTable->object[j]) < 0.0){ // checks for collision
                            phylib_bounce(&newTable->object[i], &newTable->object[j]); // if there is a collision bounce the balls and return newTable
                            newTable->time += time;
                            return newTable;
                        }
                    }
                }
                if (phylib_stopped(newTable->object[i])) { // checks if a ball has stopped rolling 
                    killLoop = 1; // Stop the loop if any rolling ball has stopped
                }
            }
        }        
        time += PHYLIB_SIM_RATE; // increments time by sim rate    
    }
    newTable->time += time; // Update the newTable time
    return newTable; // returns the newTable
}

char *phylib_object_string( phylib_object *object ){
    static char string[80];
    if (object==NULL){
        snprintf( string, 80, "NULL;" );
        return string;
    }
    switch (object->type){
        case PHYLIB_STILL_BALL:
            snprintf( string, 80,
                "STILL_BALL (%d,%6.1lf,%6.1lf)",
                object->obj.still_ball.number,
                object->obj.still_ball.pos.x,
                object->obj.still_ball.pos.y );
        break;
        case PHYLIB_ROLLING_BALL:
            snprintf( string, 80,
                "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
                object->obj.rolling_ball.number,
                object->obj.rolling_ball.pos.x,
                object->obj.rolling_ball.pos.y,
                object->obj.rolling_ball.vel.x,
                object->obj.rolling_ball.vel.y,
                object->obj.rolling_ball.acc.x,
                object->obj.rolling_ball.acc.y );
        break;
        case PHYLIB_HOLE:
            snprintf( string, 80,
                "HOLE (%6.1lf,%6.1lf)",
                object->obj.hole.pos.x,
                object->obj.hole.pos.y );
        break;
        case PHYLIB_HCUSHION:
            snprintf( string, 80,
                "HCUSHION (%6.1lf)",
                object->obj.hcushion.y );
        break;
        case PHYLIB_VCUSHION:
            snprintf( string, 80,
                "VCUSHION (%6.1lf)",
                object->obj.vcushion.x );
        break;
    }
    return string;
}
















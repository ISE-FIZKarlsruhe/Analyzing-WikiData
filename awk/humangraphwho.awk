BEGIN{prev = 0; criterion=0; human=0; printing=0; i=0}
{
#Reset if value differs from previously viewed
if($1+0 != prev){
    human = 0;  
    criterion = 0;
    printing = 0;
    i = 0;}

#Keep printing if currently viewed node has already passed all criteria (below)
if($1+0 == prev && printing==1){
    print $1";"$2} 

#save value to memory
if(printing==0){
    memory[i] = $1";"$2}

#set criterion values to 'true' if they are met
if($2+0 == 183+0) criterion = 1;
if($2+0 == 5+0) human = 1;

#if all criteria are met, print the current memory and allow all further occurences to be printed
if(criterion==1 && human==1 && printing==0){
    for (j = 0; j <= i; j++){
        print memory[j];
    }
    printing = 1}

#increment memory index    
i++;
#set previous to current
prev = $1
}
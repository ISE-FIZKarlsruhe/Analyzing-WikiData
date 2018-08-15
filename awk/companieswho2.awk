BEGIN{FS=";"; prev = 0; count = 0; printing=0; i=0; threshold=4}
{
#Reset if value differs from previously viewed
if($1+0 != prev){ 
    count = 0;
    printing = 0;
    i = 0
    criterion = 0}

count ++;

#check if criterion is there
if($3==183){
	criterion=1
}

#Keep printing if currently viewed node has already passed all criteria (below)
if($1+0 == prev && printing==1){
    print $1";"$2";"$3} 

#save value to memory
if(printing==0){
    memory[i] = $1";"$2";"$3}


#if all criteria are met, print the current memory and allow all further occurences to be printed
if(count>=threshold && criterion==1 && printing==0){
    for (j = 0; j <= i; j++){
        print memory[j];
    }
    printing = 1}

#increment memory index    
i++;
#set previous to current
prev = $1
}
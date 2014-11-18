function total_count (word_count){
	var total = 0;
	var i = word_count.length;
	while(--i){
		total += word_count[i][1];
	}
	return total;
}
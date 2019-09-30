package main

import (
	"time"
	"fmt"
	"math/rand"
	"math"
)

func generate_point(P int, collect_ch chan [2]float64) {
	
	s := rand.NewSource(time.Now().UnixNano())
	r := rand.New(s)
	
	for i := 0; i < P; i++ {
	
		x := r.Float64()
		y := r.Float64()
	
		point := [2]float64{x, y}
		collect_ch <- point
	}
}

func collect_points(P int, M int, T int) {

	collect_ch := make(chan [2]float64, P * T)
	
	for i := 0; i < T; i++ {
		go generate_point(P, collect_ch)
	}
	
	in_num, out_num := 0, 0
	var p [2]float64

	for count := 0; count < P * T; count++ {
		
		if count > 0 && count % M == 0 {
			fmt.Printf("Pi estimated: %f\n", 4.0 * float64(in_num) / float64(count))		
		}
			
		p = <- collect_ch
		x, y := p[0], p[1]
		
		if math.Pow(x-0.5, 2) + math.Pow(y-0.5, 2) < 0.25 {
			in_num += 1
		} else {
			out_num += 1
		}
	}
	
	fmt.Printf("Pi estimated: %f\n", 4.0 * float64(in_num) / float64(in_num + out_num))		
}

func main(){
	
	P, M, T := 10000, 2000, 3
	collect_points(P, M, T)
}
<?php

    function fib($n)
    {
        //Функция для вывода чисел Фибаначи
	$i = 2;
	$num1 = 0;
	$num2 = 1;
	echo $num1. '</br>';
	echo $num2. '</br>';
	while ($i < $n) {
	    $num = $num1 + $num2;
	    echo $num. '</br>';
	    $num1 = $num2;
	    $num2 = $num;
	    $i += 1;
	}
    }
    //Вывод результата
    fib(64);

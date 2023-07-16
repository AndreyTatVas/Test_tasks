<?php

    require_once 'classFigure.php';

    class classTriangle extends classFigure
    {
        //Класс для треугольников
        public $a, $b, $c;

        public function __construct($a, $b, $c)
        {
            $this->name = 'Треугольник';
            $this->a = $a;
            $this->b = $b;
            $this->c = $c;
            $this->perimeter = $this->a + $this->b + $this->c;
            $this->area = sqrt($this->perimeter / 2 *
                ($this->perimeter / 2 - $this->a) *
                ($this->perimeter / 2 - $this->b) *
                ($this->perimeter / 2 - $this->c));
        }
    }

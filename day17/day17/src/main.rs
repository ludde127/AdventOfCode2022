extern crate core;


use std::fs;
use fs::read_to_string;
use std::collections::HashSet;
use std::fmt::{Display, Formatter, write};
use std::io::ErrorKind::TimedOut;
use ndarray::{arr2, Array2, Shape, Array};

struct Tower {
    width: usize,
    occupied: HashSet<(usize, usize)>,
    highest_block: usize
}

impl Display for Tower {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        let max = self.occupied.iter().map(|e| e.1).max().unwrap_or(0);
        write!(f, "---{:?}\n", self.occupied);

        for y in 0..max+1 {

            write!(f, "|");
            for x in 0..7 {
                if self.occupied.contains(&(x, max+1-y)) {
                    write!(f, "x");
                } else {
                    write!(f, ".");
                }
            }
            write!(f, "|\n");

        }
        Ok(())
    }
}

impl Tower {
    fn new(width: usize) -> Self {
        Self {
            width,
            occupied: HashSet::new(),
            highest_block: 0
        }
    }
}

enum Shapes {
    I,
    Square,
    RevL,
    Plus,
    Line
}

impl Shapes {
    fn order() -> Vec<Array2<u8>> {
        use Shapes::*;
        vec![Shapes::get_matrix(&Line),
             Shapes::get_matrix(&Plus),
             Shapes::get_matrix(&RevL),
             Shapes::get_matrix(&I),
             Shapes::get_matrix(&Square)]
    }

    fn matrix_to_coordinates(array: &Array2<u8>) -> HashSet<(usize, usize)> {
        let mut res = HashSet::new();
        for x in 0..4 {
            for y in 0..4 {
                if *array.row(y).get(x).unwrap() == 1 {
                    res.insert((x, y));
                }
            }
        }
        println!("{:?}", res);
        println!("{:?}", array);
        res
    }

    fn get_matrix(shape: &Shapes) -> Array2<u8> {
        use Shapes::*;
        match shape {
            I => arr2(&[[1, 0, 0, 0],
                            [1, 0, 0, 0],
                            [1, 0, 0, 0],
                            [1, 0, 0, 0]]),

            Square => arr2(&[[1, 1, 0, 0],
                                 [1, 1, 0, 0],
                                 [0, 0, 0, 0],
                                 [0, 0, 0, 0]]),

            RevL => arr2(&[[0, 0, 1, 0],
                               [0, 0, 1, 0],
                               [1, 1, 1, 0],
                               [0, 0, 0, 0]]),

            Plus => arr2(&[[0, 1, 0, 0],
                               [1, 1, 1, 0],
                               [0, 1, 0, 0],
                               [0, 0, 0, 0]]),

            Line => arr2(&[[1, 1, 1, 1],
                               [0, 0, 0, 0],
                               [0, 0, 0, 0],
                               [0, 0, 0, 0]])
        }
    }
}


fn partone(data: &str, tower: &mut Tower, blocks_to_drop: usize) {
    let mut pos_in_data: usize = 0;
    let mut blocks_dropped = 0;
    let chars: Vec<char> = data.chars().collect();
    assert!(data.chars().all(|c| c == '>' || c == '<'));
    let mut cont = true;
    while cont {
        for shape in Shapes::order() {
            let points = Shapes::matrix_to_coordinates(&shape);
            let left_edge = points.iter().map(|e| e.0).min().unwrap();
            let lower_edge = points.iter().map(|e| e.1).max().unwrap();
            //assert!(false);
            let mut collision = false;
            let mut y: usize = tower.highest_block+3; //n+b = 3  n=3-b
            let mut x: usize = 2-left_edge;
            while !collision {
                let char_is_r = *chars.get(pos_in_data%chars.len()).unwrap() == '>';
                let mut dx = if char_is_r {
                                  1
                             } else {-1};
                pos_in_data+=1;
                let mut dy = -1;
                for point in &points {
                    println!("{}|{}", point.1, y);
                    let i8x = (point.0 as i8 + dx + x as i8);
                    if i8x < 0 || i8x > (tower.width - 1) as i8 {
                        dx = 0;
                        break
                    } else if tower.occupied.contains(&(i8x as usize, y+point.1)) {
                        dx = 0;
                        break
                    }
                }

                for point in &points {
                    let iy = (dy as i64 + y as i64 + point.1 as i64);
                    let ix = (point.0 as i8 + dx + x as i8);
                    println!("{}", iy);
                    if iy == 0 {
                        dy = 0;
                        break
                    } else if tower.occupied.contains(&(ix as usize, iy as usize)) {
                        dy = 0;
                        break
                    }
                }
                if dy == 0 {
                    break
                }
                x = (x as i8 + dx) as usize;
                y = (y as i64 + dy as i64) as usize;
            }

            for point in &points {
                let iy = (y as i64 + (point.1 as i64)) as usize;
                let ix = (point.0 as i8 + x as i8) as usize;
                if iy > tower.highest_block {
                    tower.highest_block = iy;
                }
                tower.occupied.insert((ix, iy));
            }
            println!("{}", tower);
            blocks_dropped+=1;
            if blocks_to_drop - blocks_dropped == 0 {
                cont = false;
                break
            }
        }

    }

}

fn main() {
    println!("Hello, world!");
    let fake = read_to_string("src/input.txt").expect("Could not read file");
    let real = read_to_string("src/input_real.txt").expect("Could not read real.");
    println!("{}", fake);
    let mut tower = Tower::new(7);
    partone(&fake, &mut tower, 3);
    println!("{}", tower.highest_block)

}

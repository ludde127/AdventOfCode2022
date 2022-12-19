use std::{fs, env};
use std::collections::{HashSet, HashMap};


fn parse_input(input: &str) -> (HashMap<String, u32>, HashMap<String, HashSet<String>>) {
    let mut vertices = HashMap::new();
    let mut edges = HashMap::new();
    for row in input.split("\n") {
        let splat: Vec<&str> = row.split(";").collect();

        let rate = splat[0].split("=").last().unwrap().parse().unwrap();
        let space_splat_all: Vec<&str> = row.split(" ").collect();
        vertices.insert(space_splat_all[1].to_string(), rate);
    }
    for row in input.split("\n") {
        let splat: Vec<&str> = row.split(";").collect();
        let space_splat_all: Vec<&str> = row.split(" ").collect();

        let space_splat_all: Vec<&str> = row.split(" ").collect();
        for potential_vert in splat[1].split(" ") {
            let temp = potential_vert.replace(",", "");
            if temp.to_uppercase() == temp && temp.len() > 0 {
                if !edges.contains_key(&space_splat_all[1].to_string()) {
                    edges.insert(space_splat_all[1].to_string(), HashSet::new());
                }
                edges.get_mut(&space_splat_all[1].to_string()).unwrap().insert(potential_vert.to_string());
            }
        }
    }
    (vertices, edges)
}

fn value_of_vertex(rate: u32, time_left: u8, distance_to:u8) -> u64 {
    ((time_left as u64) - (distance_to as u64)) * (rate as u64)
}

fn distance_between_vertices(v1: &String, v2: &String, edges: &HashMap<String, HashSet<String>>, current_depth: u32) -> u32 {
    if v1 == v2 && current_depth == 0 {
        0
    } else if v1 == v2 && current_depth != 0 {
        return current_depth
    else
    } else {
        let rec_results: u32 = 1000000;
        for next in edges.get(v1).unwrap() {
            let dist = distance_between_vertices(next, v2)
        }
        rec_results
    }
}

fn all_distances(edges: &HashMap<String, HashSet<String>>){
    let vertices: HashSet<&String> = edges.keys().collect();
    let mut distances:HashMap<&String, HashMap<&String, u32>> = HashMap::new();
    for v1 in vertices {
        for v2 in vertices {
            distances[v1][v2] = distance_between_vertices(&vertices);
        }
    }
}


fn partone(vertices: &HashMap<String, u32>, edges: &HashMap<String, HashSet<String>>, time_left: u8, current: &str, visited: &HashSet<&str>){
    for neighbor in edges.get(current) {
        if
    }

}

fn main() {

    println!("Hello, world!");
    let temp = env::current_dir().unwrap();
    let curr = temp.to_str().expect("adsad");
    let fake = fs::read_to_string(format!("{}/{}", curr, "input.txt")).expect("Could not read");
    let real = fs::read_to_string(format!("{}/{}", curr, "input_real.txt")).expect("Could not read");
    let (vertices, edges) = parse_input(&fake);

    partone(&vertices, &edges, 30, "AA", &HashSet::new());
}

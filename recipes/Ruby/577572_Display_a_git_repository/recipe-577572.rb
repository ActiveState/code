#!/usr/bin/env ruby

require 'grit'

$commits = {}

def commit_node_label(commit)
  return "#{commit.id.slice 0,5}\\n(#{commit.message.split("\n")[0]})"
end

def plot_tree (commit)
  if $commits.has_key? commit.id
    return
  else
    $commits[commit.id] = 1
  
    commit.parents.each do |c|
      puts "\"#{commit_node_label commit}\" -> \"#{commit_node_label c}\";"
      plot_tree(c)
    end
  end
end

def plot_tags(repo)
  repo.tags.each do |tag|
    puts "\"#{tag.name}\" -> \"#{commit_node_label tag.commit}\";"
    puts "\"#{tag.name}\" [shape=box, style=filled, color = yellow];"
  end
end

def draw_head(repo)
  head = repo.head.name;
  puts "\"HEAD\"  [shape=box, style=filled, color = green];"
  puts "\"HEAD\" -> \"#{head}\";"
end
  
def draw_branch_heads(repo)
  repo.branches.each do |b| 
    puts "\"#{b.name}\" -> \"#{commit_node_label b.commit}\";"
    puts "\"#{b.name}\" [shape=polygon, sides=6, style=filled, color = red];"
    plot_tree(b.commit)
  end  
end

puts "Digraph F {"
puts 'ranksep=0.5; size = "17.5,7.5"; rankdir=RL;'
repo = Grit::Repo.new(ARGV[0]);
draw_branch_heads(repo)
plot_tags(repo)
draw_head(repo)
puts "}"  
  

using DrWatson
@quickactivate "Ring Attractor"

mutable struct CircularIndex
       val::Int
       per::Int
end

function ++(x::CircularIndex)
       x.val = x.val % x.per + 1
end

function include_everywhere(filepath)
    fullpath = joinpath(@__DIR__, filepath)
    @sync for p in procs()
        @async remotecall_wait(include, p, fullpath)
    end
end

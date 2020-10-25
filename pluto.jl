### A Pluto.jl notebook ###
# v0.12.4

using Markdown
using InteractiveUtils

# This Pluto notebook uses @bind for interactivity. When running this notebook outside of Pluto, the following 'mock version' of @bind gives bound variables a default value (instead of an error).
macro bind(def, element)
    quote
        local el = $(esc(element))
        global $(esc(def)) = Core.applicable(Base.get, el) ? Base.get(el) : missing
        el
    end
end

# ╔═╡ cfc83238-15fa-11eb-3f2a-eb6ad22a7b4a
using Plots

# ╔═╡ caa74b54-15fa-11eb-3a94-67c60ebac390
@bind a1 html"<input type='range'>"

# ╔═╡ e150baec-15fb-11eb-3453-8b4b79ffd11f
@bind b1 html"<input type='range'>"

# ╔═╡ 7ea638a4-15fb-11eb-0b5c-a31e6ace1498
b = (b1-50)/10 * 0.5761298343288906

# ╔═╡ 7b4158d6-15fd-11eb-2845-ed64e8de08ad
a = (a1-50)/10 * 602.7138882757657

# ╔═╡ be3ca666-15fa-11eb-1b7b-b11ba9d3a0cb
begin
	w0 = 0.05
	inc = 0.1
	wmax = 0.25
	
	w = zeros(2000)
	w[1] = w0
	for t in 1:1999
		if t % 11 == 0
			w[t] += inc
		end
	
		w[t+1] =  w[t] - a*exp(-t/b)*0.001
		if w[t+1] < w0
			w[t+1] = w0
		elseif w[t+1] > wmax
			w[t+1] = wmax
		end
	end
	plot(w)
	
end

# ╔═╡ Cell order:
# ╠═cfc83238-15fa-11eb-3f2a-eb6ad22a7b4a
# ╠═caa74b54-15fa-11eb-3a94-67c60ebac390
# ╠═e150baec-15fb-11eb-3453-8b4b79ffd11f
# ╠═7ea638a4-15fb-11eb-0b5c-a31e6ace1498
# ╠═7b4158d6-15fd-11eb-2845-ed64e8de08ad
# ╠═be3ca666-15fa-11eb-1b7b-b11ba9d3a0cb
